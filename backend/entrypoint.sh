#!/bin/sh
set -e

echo "=========================================================="
echo "🦚 PEACOCK WEDDING SYSTEM – BACKEND INITIALIZATION"
echo "=========================================================="

# 1. Wait for MySQL to become ready
echo "⏳ Checking database connectivity..."
python scripts/wait_for_db.py || {
    echo "⚠️ Database wait failed or timed out, continuing startup..."
}

# 2. Run Database Migrations (Alembic)
echo "🔄 Running database migrations (Alembic)..."
alembic upgrade head || {
    echo "⚠️ Alembic upgrade finished with notice; FastAPI will ensure schemas on startup."
}

# 3. Seed Initial Demo Data (Venues, Admin, Menus, Cards)
echo "🌱 Seeding initial demo data (idempotent)..."
python scripts/seed_data.py || {
    echo "⚠️ Seed data notice (continuing)..."
}

# 4. Start Uvicorn Server
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
WORKERS="${WORKERS:-2}"

echo "🚀 Starting Uvicorn server on http://${HOST}:${PORT} with ${WORKERS} worker(s)..."
exec uvicorn app.main:app --host "${HOST}" --port "${PORT}" --workers "${WORKERS}"
