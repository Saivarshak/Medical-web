from __future__ import annotations

import base64
import json
import mimetypes
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import httpx
from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config import get_settings

settings = get_settings()

app = FastAPI(
    title="RapidAid AI API",
    description=(
        "AI-assisted emergency scanner APIs. Guidance is informational only and "
        "is not a substitute for emergency services or professional medical care."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
ALERTS_PATH = DATA_DIR / "alerts.json"
SCAN_HISTORY_PATH = DATA_DIR / "scan_history.json"

Severity = Literal["Low", "Moderate", "High", "Critical"]


class VisionAnalyzeRequest(BaseModel):
    image_id: str | None = None
    image_base64: str | None = None
    mime_type: str = "image/jpeg"
    symptoms: str | None = None
    age: int | None = Field(default=None, ge=0, le=120)
    location_hint: str | None = None


class Hospital(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    distance_km: float
    emergency: bool = True


class WhatsAppRequest(BaseModel):
    phone_number: str | None = None
    patient_name: str = "RapidAid AI user"
    severity: Severity
    summary: str
    location_url: str | None = None


class Alert(BaseModel):
    id: str
    created_at: str
    channel: str
    recipient: str
    severity: Severity
    message: str
    status: str


DISCLAIMER = (
    "RapidAid AI provides AI-assisted guidance only and is not a substitute for "
    "professional medical diagnosis or emergency services. If symptoms are severe, "
    "worsening, or life-threatening, call local emergency services immediately."
)

FIRST_AID_BY_SEVERITY: dict[Severity, list[str]] = {
    "Low": [
        "Clean minor wounds with clean running water.",
        "Apply gentle pressure if there is light bleeding.",
        "Cover with a sterile dressing and monitor for infection.",
    ],
    "Moderate": [
        "Stop activity and keep the injured area still.",
        "Apply pressure to bleeding with sterile gauze or clean cloth.",
        "Use a cold pack wrapped in cloth for swelling, 15-20 minutes at a time.",
        "Seek same-day medical advice if pain, swelling, or bleeding persists.",
    ],
    "High": [
        "Call a local emergency number or go to the nearest emergency department.",
        "Keep the person still, warm, and reassured.",
        "Apply firm pressure to significant bleeding; do not remove embedded objects.",
        "Do not give food or drink if surgery or sedation may be needed.",
    ],
    "Critical": [
        "Call emergency services immediately.",
        "Check breathing and responsiveness; begin CPR if trained and needed.",
        "Control severe bleeding with firm continuous pressure.",
        "Keep the airway clear and do not move the person unless they are in danger.",
    ],
}

DEMO_HOSPITALS = [
    Hospital(
        name="City General Emergency Hospital",
        address="24 Care Street, Central District",
        latitude=17.385,
        longitude=78.4867,
        distance_km=1.4,
    ),
    Hospital(
        name="Rapid Trauma & Critical Care",
        address="8 LifeLine Road, Medical Zone",
        latitude=17.3921,
        longitude=78.4812,
        distance_km=2.1,
    ),
    Hospital(
        name="Community First Aid Clinic",
        address="12 Health Avenue, North Block",
        latitude=17.399,
        longitude=78.49,
        distance_km=3.3,
        emergency=False,
    ),
]


def ensure_data_dirs() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for path in (ALERTS_PATH, SCAN_HISTORY_PATH):
        if not path.exists():
            path.write_text("[]", encoding="utf-8")


def read_json_list(path: Path) -> list[dict[str, Any]]:
    ensure_data_dirs()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def append_json(path: Path, item: dict[str, Any]) -> None:
    items = read_json_list(path)
    items.insert(0, item)
    path.write_text(json.dumps(items[:100], indent=2), encoding="utf-8")


def strip_data_url(image_base64: str) -> str:
    if "," in image_base64 and image_base64.strip().startswith("data:"):
        return image_base64.split(",", 1)[1]
    return image_base64


def infer_demo_severity(symptoms: str | None) -> Severity:
    text = (symptoms or "").lower()
    critical_words = ["unconscious", "not breathing", "heavy bleeding", "severe bleeding", "amputation"]
    high_words = ["deep", "fracture", "burn", "large", "swollen", "infection", "pus"]
    moderate_words = ["pain", "bleeding", "cut", "sprain", "bruise"]
    if any(word in text for word in critical_words):
        return "Critical"
    if any(word in text for word in high_words):
        return "High"
    if any(word in text for word in moderate_words):
        return "Moderate"
    return "Low"


def safe_json_from_text(text: str) -> dict[str, Any] | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return None
    return None


async def analyze_with_gemini(payload: VisionAnalyzeRequest) -> dict[str, Any] | None:
    if not settings.gemini_api_key or not payload.image_base64:
        return None

    prompt = f"""
You are RapidAid AI, an emergency first-aid assistant. Analyze the injury/medical image.
Return strict JSON only with keys:
severity: one of Low, Moderate, High, Critical
detected_issue: short plain-language observation
confidence: number from 0 to 1
first_aid: array of 3-5 safe first-aid steps
red_flags: array of urgent warning signs
recommended_action: concise next step
Do not diagnose. Include uncertainty where appropriate.
User symptoms/context: {payload.symptoms or "not provided"}
Age: {payload.age or "not provided"}
Location hint: {payload.location_hint or "not provided"}
"""

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:"
        f"generateContent?key={settings.gemini_api_key}"
    )
    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": payload.mime_type,
                            "data": strip_data_url(payload.image_base64),
                        }
                    },
                ]
            }
        ],
        "generationConfig": {"temperature": 0.2, "response_mime_type": "application/json"},
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=request_body)
        response.raise_for_status()
    except Exception:
        return None

    try:
        candidates = response.json().get("candidates", [])
        text = candidates[0]["content"]["parts"][0].get("text", "") if candidates else ""
        return safe_json_from_text(text)
    except Exception:
        return None


def normalize_analysis(raw: dict[str, Any] | None, symptoms: str | None) -> dict[str, Any]:
    severity = raw.get("severity") if raw else infer_demo_severity(symptoms)
    if severity not in FIRST_AID_BY_SEVERITY:
        severity = infer_demo_severity(symptoms)

    detected_issue = raw.get("detected_issue") if raw else None
    first_aid = raw.get("first_aid") if raw else None
    red_flags = raw.get("red_flags") if raw else None

    return {
        "scan_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "severity": severity,
        "detected_issue": detected_issue or "Possible visible injury or medical concern detected from the provided image.",
        "confidence": float(raw.get("confidence", 0.62)) if raw else 0.62,
        "first_aid": first_aid if isinstance(first_aid, list) and first_aid else FIRST_AID_BY_SEVERITY[severity],
        "red_flags": red_flags
        if isinstance(red_flags, list) and red_flags
        else [
            "Difficulty breathing, confusion, fainting, or chest pain",
            "Severe or uncontrolled bleeding",
            "Rapidly worsening pain, swelling, fever, or spreading redness",
        ],
        "recommended_action": raw.get("recommended_action")
        if raw
        else (
            "Seek emergency care now."
            if severity in {"High", "Critical"}
            else "Monitor closely and consult a clinician if symptoms worsen."
        ),
        "nearby_hospitals": [hospital.model_dump() for hospital in DEMO_HOSPITALS],
        "disclaimer": DISCLAIMER,
        "demo_mode": raw is None,
    }


@app.on_event("startup")
def startup() -> None:
    ensure_data_dirs()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)) -> dict[str, Any]:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image file.")

    suffix = Path(file.filename or "").suffix or mimetypes.guess_extension(file.content_type) or ".jpg"
    image_id = f"{uuid.uuid4()}{suffix}"
    destination = UPLOAD_DIR / image_id
    content = await file.read()
    destination.write_bytes(content)

    return {
        "image_id": image_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
        "message": "Image uploaded successfully.",
    }


@app.post("/vision-analyze")
async def vision_analyze(payload: VisionAnalyzeRequest) -> dict[str, Any]:
    if payload.image_id and not payload.image_base64:
        image_path = UPLOAD_DIR / payload.image_id
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Uploaded image not found.")
        payload.image_base64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        payload.mime_type = mimetypes.guess_type(image_path.name)[0] or payload.mime_type

    if not payload.image_base64:
        raise HTTPException(status_code=400, detail="Provide image_id or image_base64 for analysis.")

    raw_analysis = await analyze_with_gemini(payload)
    analysis = normalize_analysis(raw_analysis, payload.symptoms)
    analysis["image_id"] = payload.image_id
    analysis["symptoms"] = payload.symptoms
    append_json(SCAN_HISTORY_PATH, analysis)
    return analysis


@app.get("/nearest-hospitals")
def nearest_hospitals(
    lat: float | None = Query(default=None, description="Latitude from browser geolocation"),
    lon: float | None = Query(default=None, description="Longitude from browser geolocation"),
) -> dict[str, Any]:
    return {
        "source": "demo" if lat is None or lon is None else "openstreetmap-ready-demo",
        "hospitals": [hospital.model_dump() for hospital in DEMO_HOSPITALS],
        "note": "Connect an OpenStreetMap/Overpass lookup in production for live nearby facilities.",
    }


@app.post("/send-whatsapp")
async def send_whatsapp(payload: WhatsAppRequest) -> Alert:
    recipient = payload.phone_number or settings.default_emergency_contact
    if not recipient:
        raise HTTPException(status_code=400, detail="No emergency contact phone number configured.")

    message = (
        f"Emergency alert from RapidAid AI for {payload.patient_name}. "
        f"Severity: {payload.severity}. Summary: {payload.summary}. "
        f"{'Location: ' + payload.location_url if payload.location_url else ''} "
        f"{DISCLAIMER}"
    )
    status = "queued-demo"

    if settings.whatsapp_access_token and settings.whatsapp_phone_number_id:
        url = f"https://graph.facebook.com/v20.0/{settings.whatsapp_phone_number_id}/messages"
        headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
        body = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": True, "body": message},
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, headers=headers, json=body)
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail="WhatsApp Business alert failed.")
        status = "sent"

    alert = Alert(
        id=str(uuid.uuid4()),
        created_at=datetime.now(timezone.utc).isoformat(),
        channel="whatsapp",
        recipient=recipient,
        severity=payload.severity,
        message=message,
        status=status,
    )
    append_json(ALERTS_PATH, alert.model_dump())
    return alert


@app.get("/alerts")
def alerts() -> dict[str, list[dict[str, Any]]]:
    return {"alerts": read_json_list(ALERTS_PATH)}

