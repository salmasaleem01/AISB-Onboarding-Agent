# Backend - Bootcamp Onboarding Platform

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Notes
- SQLite database path: `backend/onboarding.db`
- Uploads stored in `backend/uploads/`
- CORS is open for MVP
