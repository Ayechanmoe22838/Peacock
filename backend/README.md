# Backend Architecture & Deployment – PEACOCK

This folder contains the Docker and deployment configuration for the **PEACOCK** backend application service.

---

## 🏗️ Architecture Overview

The backend is built with **FastAPI**, **SQLAlchemy 2.0 ORM**, **PyMySQL**, **Pydantic v2**, and **Alembic**:

- `app/main.py`: Main FastAPI application, middleware, static/media mounts, and healthcheck `/health`.
- `app/core/`: Application configuration (`config.py`), database engine (`database.py`), Fernet phone encryption (`encryption.py`), and RBAC security (`security.py`).
- `app/models/`: 22 normalized relational models.
- `app/schemas/`: Pydantic request and response schemas.
- `app/routers/`: Route controllers (`auth`, `public`, `customer`, `admin`).
- `app/services/`: Core business logic services (`booking_service`, `payment_service`, `budget_service`, `report_service`, `encryption_service`, `notification_service`).
- `alembic/`: Database migrations.
- `scripts/wait_for_db.py`: Database readiness probe before running migrations.
- `scripts/seed_data.py`: Idempotent database seeder (initializes Admin, Cherry, Venues, Menus, Invitation Cards).

---

## 🐳 Docker Deployment

### Building the Image Locally
```bash
docker build -t peacock-backend -f backend/Dockerfile .
```

### Running the Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="mysql+pymysql://root:root@host.docker.internal:3306/peacock_db?charset=utf8mb4" \
  -e SECRET_KEY="peacock-secret-key-secure-wedding-system-2026" \
  -e PORT=8000 \
  peacock-backend
```

---

## 🚂 Railway Deployment

Railway automatically injects environment variables for connected MySQL plugins.

### Required Environment Variables on Railway:
- `MYSQL_URL` or `DATABASE_URL`: Automatically provided by Railway's MySQL plugin. The application auto-detects `mysql://` and converts it to `mysql+pymysql://`.
- `PORT`: Automatically provided by Railway (e.g. `8080`).
- `SECRET_KEY`: A secure random secret key (e.g., generated with `openssl rand -hex 32`).
- `FERNET_KEY`: (Optional) Derived from `SECRET_KEY` if omitted.

### Railway Configuration (`backend/railway.json`):
```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "backend/Dockerfile"
  },
  "deploy": {
    "startCommand": "./entrypoint.sh",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

The container automatically executes `backend/entrypoint.sh`, which:
1. Waits for MySQL to be healthy.
2. Applies Alembic migrations (`alembic upgrade head`).
3. Seeds default venues, food items, and demo accounts (if database is newly initialized).
4. Launches Uvicorn on `0.0.0.0:$PORT`.
