# RapidAid AI

AI Vision Emergency Scanner for emergency first-aid guidance.

RapidAid AI lets a user upload or capture an image of an injury or medical issue. The backend can send the image to Gemini Vision, estimate severity, return first-aid recommendations, surface nearby hospitals on an OpenStreetMap/Leaflet map, save scan history, and queue/send WhatsApp Business emergency alerts for High or Critical cases.

> Disclaimer: RapidAid AI provides AI-assisted guidance only. It is not a medical diagnosis or a substitute for professional medical care or emergency services.

## Stack

- Frontend: React + Bootstrap 5 + Leaflet
- Backend: FastAPI
- Database/storage target: Supabase PostgreSQL + Storage
- AI target: Gemini Vision API
- Auth target: JWT
- Deployment target: Vercel + Render

## API

- `POST /upload-image`
- `POST /vision-analyze`
- `GET /nearest-hospitals`
- `POST /send-whatsapp`
- `GET /alerts`
- `GET /health`

## Local development

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Copy `backend/.env.example` to `backend/.env` and fill in production keys for Gemini, Supabase, JWT, and WhatsApp Business.
