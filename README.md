# Bootcamp Onboarding Platform (MVP)

Monorepo with FastAPI backend and Next.js frontend.

## Structure
- `/backend`: FastAPI, SQLite, simple CrewAI-style agents
- `/frontend`: Next.js 14 + TailwindCSS

## Quickstart

Backend:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend
```

Frontend:
```bash
cd frontend
pnpm install # or npm/yarn
cp .env.local.example .env.local || true
# Ensure NEXT_PUBLIC_API_BASE=http://localhost:8000
pnpm dev
```

## Deployment
- Backend: Deploy the `backend` directory to Railway/Render.
  - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Env: `DATABASE_URL` (optional for external DB)
- Frontend: Deploy `frontend` to Vercel.
  - Env: `NEXT_PUBLIC_API_BASE=https://<backend-domain>`

## API Endpoints
- POST `/apply`
- GET `/screen-applications`
- POST `/quiz/generate`
- POST `/quiz/submit`
- POST `/video/upload`
- GET `/final-selection`
- POST `/attendance`
- POST `/assignments/upload`

