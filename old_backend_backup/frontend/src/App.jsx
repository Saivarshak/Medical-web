import { useMemo, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const severityOrder = {
  Low: 1,
  Moderate: 2,
  High: 3,
  Critical: 4,
};

const defaultHospitals = [
  {
    name: "City General Emergency Hospital",
    address: "24 Care Street, Central District",
    latitude: 17.385,
    longitude: 78.4867,
    distance_km: 1.4,
    emergency: true,
  },
];

function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function App() {
  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [age, setAge] = useState("");
  const [patientName, setPatientName] = useState("");
  const [contact, setContact] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [alerting, setAlerting] = useState(false);
  const [error, setError] = useState("");

  const hospitals = analysis?.nearby_hospitals?.length ? analysis.nearby_hospitals : defaultHospitals;
  const mapCenter = useMemo(() => [hospitals[0].latitude, hospitals[0].longitude], [hospitals]);
  const shouldShowAlert = analysis && severityOrder[analysis.severity] >= severityOrder.High;

  async function handleFileChange(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    setImageFile(file);
    setPreview(await fileToDataUrl(file));
    setAnalysis(null);
    setError("");
  }

  async function analyzeImage(event) {
    event.preventDefault();
    if (!imageFile || !preview) {
      setError("Please capture or upload an injury image first.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/vision-analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          image_base64: preview,
          mime_type: imageFile.type || "image/jpeg",
          symptoms,
          age: age ? Number(age) : null,
        }),
      });
      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(detail.detail || "Image analysis failed.");
      }
      const data = await response.json();
      setAnalysis(data);
      if (severityOrder[data.severity] >= severityOrder.High) {
        loadAlerts();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function sendWhatsAppAlert() {
    if (!analysis) return;
    setAlerting(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/send-whatsapp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone_number: contact || null,
          patient_name: patientName || "RapidAid AI user",
          severity: analysis.severity,
          summary: `${analysis.detected_issue} Recommended action: ${analysis.recommended_action}`,
        }),
      });
      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(detail.detail || "WhatsApp alert failed.");
      }
      const alert = await response.json();
      setAlerts((current) => [alert, ...current]);
    } catch (err) {
      setError(err.message);
    } finally {
      setAlerting(false);
    }
  }

  async function loadAlerts() {
    try {
      const response = await fetch(`${API_BASE}/alerts`);
      if (response.ok) {
        const data = await response.json();
        setAlerts(data.alerts || []);
      }
    } catch {
      // Alert history is helpful, not required for emergency guidance.
    }
  }

  return (
    <div>
      <section className="hero py-5">
        <div className="container py-4">
          <div className="row align-items-center g-4">
            <div className="col-lg-7">
              <span className="badge text-bg-light text-danger mb-3">AI Vision Emergency Scanner</span>
              <h1 className="display-5 fw-bold mb-3">RapidAid AI turns an injury image into first-aid next steps.</h1>
              <p className="lead mb-4">
                Upload or capture a photo, estimate severity, review safe first-aid guidance, find nearby care, and
                trigger an approved WhatsApp emergency alert for high-risk cases.
              </p>
              <div className="alert alert-warning disclaimer mb-0">
                RapidAid AI provides AI-assisted guidance only. It is not a diagnosis or a substitute for emergency
                services.
              </div>
            </div>
            <div className="col-lg-5">
              <div className="card scanner-card">
                <div className="card-body p-4">
                  <h2 className="h4 mb-3">Scanner workflow</h2>
                  <ol className="mb-0">
                    <li>Login or continue as demo user</li>
                    <li>Upload/capture injury image</li>
                    <li>Gemini Vision analysis</li>
                    <li>Severity + first aid + hospitals</li>
                    <li>WhatsApp alert for High/Critical</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <main className="container my-5">
        <div className="row g-4">
          <div className="col-lg-5">
            <form className="card scanner-card" onSubmit={analyzeImage}>
              <div className="card-body p-4">
                <h2 className="h4 mb-3">Upload or capture image</h2>
                <div className="image-preview mb-3">
                  {preview ? <img src={preview} alt="Injury preview" /> : <span className="text-muted">Image preview</span>}
                </div>
                <input
                  className="form-control mb-3"
                  type="file"
                  accept="image/*"
                  capture="environment"
                  onChange={handleFileChange}
                />
                <label className="form-label" htmlFor="symptoms">
                  Symptoms or context
                </label>
                <textarea
                  id="symptoms"
                  className="form-control mb-3"
                  rows="3"
                  placeholder="Example: deep cut on forearm, bleeding for 10 minutes"
                  value={symptoms}
                  onChange={(event) => setSymptoms(event.target.value)}
                />
                <div className="row g-3">
                  <div className="col-sm-6">
                    <label className="form-label" htmlFor="age">
                      Age
                    </label>
                    <input
                      id="age"
                      className="form-control"
                      type="number"
                      min="0"
                      max="120"
                      value={age}
                      onChange={(event) => setAge(event.target.value)}
                    />
                  </div>
                  <div className="col-sm-6">
                    <label className="form-label" htmlFor="patient">
                      Patient name
                    </label>
                    <input
                      id="patient"
                      className="form-control"
                      value={patientName}
                      onChange={(event) => setPatientName(event.target.value)}
                    />
                  </div>
                </div>
                <button className="btn btn-danger w-100 mt-4" type="submit" disabled={loading}>
                  {loading ? "Analyzing image..." : "Analyze emergency image"}
                </button>
                {error && <div className="alert alert-danger mt-3 mb-0">{error}</div>}
              </div>
            </form>
          </div>

          <div className="col-lg-7">
            <div className="card scanner-card mb-4">
              <div className="card-body p-4">
                <div className="d-flex justify-content-between align-items-start gap-3 mb-3">
                  <div>
                    <h2 className="h4 mb-1">AI assessment</h2>
                    <p className="text-muted mb-0">Severity: Low, Moderate, High, or Critical</p>
                  </div>
                  {analysis && (
                    <span className={`badge rounded-pill severity-pill severity-${analysis.severity}`}>
                      {analysis.severity}
                    </span>
                  )}
                </div>

                {!analysis ? (
                  <p className="text-muted mb-0">
                    Results will appear here after analysis, including first-aid guidance and escalation prompts.
                  </p>
                ) : (
                  <>
                    {analysis.demo_mode && (
                      <div className="alert alert-info">
                        Demo analysis is active because no Gemini API key is configured. Add the key on the backend for
                        real vision analysis.
                      </div>
                    )}
                    <p className="fs-5">{analysis.detected_issue}</p>
                    <p>
                      <strong>Recommended action:</strong> {analysis.recommended_action}
                    </p>
                    <h3 className="h5">First-aid recommendations</h3>
                    <ul>
                      {analysis.first_aid.map((step) => (
                        <li key={step}>{step}</li>
                      ))}
                    </ul>
                    <h3 className="h5">Red flags</h3>
                    <ul className="mb-0">
                      {analysis.red_flags.map((flag) => (
                        <li key={flag}>{flag}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            </div>

            <div className="card scanner-card mb-4">
              <div className="card-body p-4">
                <h2 className="h4 mb-3">Nearby hospitals</h2>
                <div className="map-frame mb-3">
                  <MapContainer center={mapCenter} zoom={13} scrollWheelZoom={false} className="h-100 w-100">
                    <TileLayer
                      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {hospitals.map((hospital) => (
                      <Marker key={hospital.name} position={[hospital.latitude, hospital.longitude]}>
                        <Popup>
                          <strong>{hospital.name}</strong>
                          <br />
                          {hospital.address}
                        </Popup>
                      </Marker>
                    ))}
                  </MapContainer>
                </div>
                <div className="list-group">
                  {hospitals.map((hospital) => (
                    <div className="list-group-item" key={hospital.name}>
                      <div className="d-flex justify-content-between">
                        <strong>{hospital.name}</strong>
                        <span>{hospital.distance_km} km</span>
                      </div>
                      <small className="text-muted">{hospital.address}</small>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="card scanner-card">
              <div className="card-body p-4">
                <h2 className="h4 mb-3">WhatsApp emergency alert</h2>
                <p className="text-muted">
                  Enabled for High/Critical scans through an approved WhatsApp Business integration.
                </p>
                <div className="input-group mb-3">
                  <span className="input-group-text">+</span>
                  <input
                    className="form-control"
                    placeholder="Emergency contact phone with country code"
                    value={contact}
                    onChange={(event) => setContact(event.target.value)}
                  />
                </div>
                <button className="btn btn-dark" disabled={!shouldShowAlert || alerting} onClick={sendWhatsAppAlert}>
                  {alerting ? "Sending alert..." : "Send emergency WhatsApp alert"}
                </button>
                {!shouldShowAlert && (
                  <small className="d-block text-muted mt-2">Available after a High or Critical severity result.</small>
                )}
                {alerts.length > 0 && (
                  <div className="mt-4">
                    <h3 className="h6">Recent alerts</h3>
                    {alerts.slice(0, 3).map((alert) => (
                      <div className="border rounded p-2 mb-2" key={alert.id}>
                        <span className="badge text-bg-secondary me-2">{alert.status}</span>
                        <span>{alert.severity}</span>
                        <small className="d-block text-muted">{alert.recipient}</small>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
