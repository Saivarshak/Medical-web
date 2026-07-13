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

## Deploy

### Backend on Render

1. Push this repository to GitHub.
2. In Render, create a new Blueprint or Web Service from the repository.
3. Use `render.yaml` at the repository root.
4. Add these environment variables in Render:
   - `FRONTEND_ORIGIN=https://your-vercel-app.vercel.app`
   - `GEMINI_API_KEY=your_gemini_api_key`
   - optional Supabase and WhatsApp Business values from `backend/.env.example`
5. After deploy, the API should respond at:
   - `https://your-render-service.onrender.com/`
   - `https://your-render-service.onrender.com/health`
   - `https://your-render-service.onrender.com/docs`

### Frontend on Vercel

1. Import the same GitHub repository into Vercel.
2. Keep the root directory as the repository root; `vercel.json` points Vercel to `frontend`.
3. Add this Vercel environment variable:
   - `VITE_API_BASE_URL=https://your-render-service.onrender.com`
4. Deploy.
