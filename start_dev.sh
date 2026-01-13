#!/bin/bash
echo "🚀 Starting TeraVoo Local Dev Environment (Backend)..."

# 1. Start Database
echo "[1/3] Starting Database..."
docker-compose up -d db
sleep 3 # Wait for DB to be ready

# 2. Setup Python Env
echo "[2/3] Setting up Python..."
cd backend
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# 3. Run Migrations & Server
echo "[3/3] Running Migrations & Starting Server..."
alembic upgrade head
echo "✅ Server starting on http://localhost:8000"
echo "👉 Open a NEW terminal for Frontend (cd web && npm run dev)"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
