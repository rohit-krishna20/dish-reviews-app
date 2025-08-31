# Dish Reviews App

# Dish-Level Reviews App (MVP)

- Backend: FastAPI + SQLite (JWT auth)
- Frontend: Expo React Native
- Feature: Rate dishes, not whole restaurants. Start a visit, add dish reviews, robust scoring.

## Run backend
```bash
cd backend
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env   # edit SECRET_KEY to a long random string
python -m app.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
