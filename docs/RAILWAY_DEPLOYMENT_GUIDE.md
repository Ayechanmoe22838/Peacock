# Railway & Docker Deployment Guide – PEACOCK

This guide outlines how to deploy the **PEACOCK – Smart Wedding Reception Management System** to [Railway](https://railway.com) using Docker, Railway MySQL plugin, persistent volumes, and custom domains.

---

## 🏛️ Deployment Architecture Options

Railway supports two primary deployment topologies for this repository:

```
Option 1: Unified Single-Service Deployment (Recommended for simplicity & low cost)
┌─────────────────────────────────────────────────────────────┐
│                       Railway Project                       │
│                                                             │
│   ┌────────────────────────┐      ┌─────────────────────┐   │
│   │   peacock-app Service  │◄────►│   MySQL Database    │   │
│   │   (FastAPI + Jinja2)   │      │   Plugin (Railway)  │   │
│   │   Port: $PORT          │      │   Port: 3306        │   │
│   └───────────▲────────────┘      └─────────────────────┘   │
│               │ (HTTP / HTTPS)                              │
│       ┌───────┴───────┐                                     │
│       │  User / Client│                                     │
│       └───────────────┘                                     │
└─────────────────────────────────────────────────────────────┘

Option 2: Split Multi-Service Deployment (Backend + Frontend Nginx Gateway)
┌─────────────────────────────────────────────────────────────┐
│                       Railway Project                       │
│                                                             │
│   ┌────────────────────────┐      ┌─────────────────────┐   │
│   │   peacock-frontend     │      │   peacock-backend   │   │
│   │   (Nginx Gateway)      │─────►│   (FastAPI Core)    │   │
│   │   Port: $PORT          │      │   Port: 8000        │   │
│   └───────────▲────────────┘      └──────────┬──────────┘   │
│               │                              │              │
│       ┌───────┴───────┐                      ▼              │
│       │  User / Client│           ┌─────────────────────┐   │
│       └───────────────┘           │   MySQL Database    │   │
│                                   │   Plugin (Railway)  │   │
│                                   └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Option 1: Step-by-Step Deployment (Unified Single-Service)

This is the fastest, cleanest deployment method on Railway.

### Step 1: Create a Railway Project
1. Log in to [Railway](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select the `Smart Wedding Reception Management System` repository.

### Step 2: Add MySQL Database Plugin
1. In the Railway project canvas, click **+ New**.
2. Select **Database** -> **Add MySQL**.
3. Railway will provision a managed MySQL 8.0 instance and generate credentials:
   - `MYSQL_URL`
   - `MYSQLHOST`
   - `MYSQLPORT`
   - `MYSQLUSER`
   - `MYSQLPASSWORD`
   - `MYSQLDATABASE`

### Step 3: Configure Environment Variables
1. Click on the **peacock-app** web service.
2. Navigate to the **Variables** tab.
3. Railway automatically links the MySQL database variables. Ensure the following variables are present:
   - `DATABASE_URL`: `${{MySQL.MYSQL_URL}}` (or rely on `MYSQL_URL` which the backend automatically converts to `mysql+pymysql://`).
   - `SECRET_KEY`: Generate a secure random string (e.g. `peacock-secret-key-prod-2026`).
   - `ENVIRONMENT`: `production`

### Step 4: Attach Persistent Volume (For User Uploads)
To ensure venue photos, bride/groom profiles, and payment receipts persist across container deployments:
1. In your service settings, navigate to **Volumes**.
2. Click **+ Add Volume**.
3. Mount Path: `/app/media`.
4. Click **Save**.

### Step 5: Automatic Startup & Verification
Upon deployment, Railway will:
1. Build the Docker container using `Dockerfile`.
2. Run `entrypoint.sh`, which automatically:
   - Connects to MySQL using `scripts/wait_for_db.py`.
   - Runs database migrations via `alembic upgrade head`.
   - Seeds initial venues, cuisine items, and administrative accounts via `scripts/seed_data.py`.
   - Starts Uvicorn listening on `0.0.0.0:$PORT`.
3. Check the health probe at `/health`.
4. Click **Generate Domain** in the service's **Networking** tab to obtain a public URL (e.g., `https://peacock-production.up.railway.app`).

---

## 🏢 Option 2: Step-by-Step Deployment (Split Microservices)

If you prefer isolating the FastAPI API backend and the Nginx frontend reverse proxy:

### 1. Backend Service Configuration
1. In Railway, click **+ New** -> **GitHub Repo** -> select the repository.
2. Rename service to `peacock-backend`.
3. Go to **Settings** -> **Build**:
   - **Dockerfile Path**: `backend/Dockerfile`
4. Go to **Variables**:
   - `DATABASE_URL`: `${{MySQL.MYSQL_URL}}`
   - `SECRET_KEY`: `peacock-secret-key-prod-2026`
   - `PORT`: `8000`
5. Go to **Networking**:
   - Enable **Private Networking** (Railway assigns e.g. `peacock-backend.railway.internal`).

### 2. Frontend Gateway Configuration
1. Click **+ New** -> **GitHub Repo** -> select the repository.
2. Rename service to `peacock-frontend`.
3. Go to **Settings** -> **Build**:
   - **Dockerfile Path**: `frontend/Dockerfile`
4. Go to **Variables**:
   - `BACKEND_URL`: `http://${{peacock-backend.RAILWAY_PRIVATE_DOMAIN}}:8000`
5. Go to **Networking**:
   - Click **Generate Domain** (Public HTTPS).

---

## 💻 Local Testing with Docker Compose

You can test the entire multi-container production stack locally before pushing to Railway:

```bash
# 1. Start MySQL, Backend, and Frontend (Nginx) containers
docker-compose up --build

# 2. Open browser
http://localhost

# 3. View running logs
docker-compose logs -f backend

# 4. Shut down stack
docker-compose down -v
```

---

## 🔑 Default Accounts After Deployment

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@peacock.com` | `AdminPassword123!` |
| **Customer (Cherry)** | `customer@peacock.com` | `CustomerPassword123!` |

---

## 🛡️ Railway Environment Variables Reference

| Variable Name | Required | Default / Example | Purpose |
|---|---|---|---|
| `PORT` | Auto (Railway) | `8000` | Port the web service binds to. |
| `DATABASE_URL` / `MYSQL_URL` | Yes | `mysql://...` | Connection string to Railway MySQL. Backend converts `mysql://` to `mysql+pymysql://`. |
| `SECRET_KEY` | Yes | `peacock-secret-key...` | Cryptographic key for JWT tokens & AES-CBC Fernet phone encryption. |
| `ENVIRONMENT` | No | `production` | Enables production mode and disables reload. |
| `KPAY_PHONE` | No | `09450012345` | Official KPay account number for customer payments. |
| `KPAY_NAME` | No | `PEACOCK WEDDING SERVICES` | Official recipient name for wedding booking deposits. |

---

## 🛠️ Troubleshooting

### 1. Database Connection Timeout on Initial Deploy
- **Symptom**: `scripts/wait_for_db.py` reports `Database not ready yet`.
- **Cause**: MySQL plugin may take 10-15 seconds to finish its initial initialization.
- **Fix**: The entrypoint script automatically retries 30 times (60 seconds) with exponential backoff before continuing.

### 2. Port Binding Issues
- **Symptom**: Railway error: `Application failed to respond on PORT`.
- **Cause**: Application hardcoded to `127.0.0.1` or fixed port `8000`.
- **Fix**: Handled automatically! `app/core/config.py` and `entrypoint.sh` read Railway's dynamic `$PORT` environment variable and bind to `0.0.0.0`.

### 3. File Uploads Disappearing After Redeploy
- **Symptom**: Uploaded payment slips or venue photos disappear after a new commit.
- **Fix**: Attach a Railway Volume to `/app/media` in the service settings.
