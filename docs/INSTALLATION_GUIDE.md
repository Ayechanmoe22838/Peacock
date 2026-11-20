# PEACOCK – Installation & Setup Guide

This guide describes how to deploy and run the Peacock application locally on Windows.

## 1. Prerequisites
- **Python:** Python 3.10 to 3.14 (Verified on Python 3.14.3)
- **MySQL:** MySQL Server 8.0+ running on `127.0.0.1:3306`
- **Dependencies:** All listed in `requirements.txt`

## 2. Environment Configuration (`.env`)
Create or verify the `.env` file in the project root:
```ini
PROJECT_NAME=Peacock – Smart Wedding Reception Management System
SECRET_KEY=peacock-secret-key-secure-wedding-system-2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=peacock_db
DATABASE_URL=mysql+pymysql://root:root@127.0.0.1:3306/peacock_db?charset=utf8mb4

UPLOAD_DIR=media
CURRENCY_CODE=MMK
CURRENCY_SYMBOL=Ks

ADMIN_EMAIL=admin@peacock.com
ADMIN_PASSWORD=AdminPassword123!
ADMIN_NAME=Peacock Administrator

KPAY_PHONE=09450012345
KPAY_NAME=PEACOCK WEDDING SERVICES
KPAY_QR_IMAGE=/static/images/kpay_qr.png
```

## 3. Database Initialization
Ensure the MySQL database exists:
```sql
CREATE DATABASE IF NOT EXISTS peacock_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Apply database migrations:
```bash
alembic upgrade head
```

Seed realistic wedding demo data:
```bash
python scripts/seed_data.py
```

## 4. Starting the Web Server
Launch the application with Uvicorn:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Or use the convenience startup runner:
```bash
python run.py
```

Access the application in your browser:
- Public Website: `http://127.0.0.1:8000`
- Super Admin Login: `http://127.0.0.1:8000/login` (`admin@peacock.com` / `AdminPassword123!`)
- Demo Customer Login: `customer@peacock.com` / `CustomerPassword123!`

## 5. Running Automated Tests
Execute the full test suite with Pytest:
```bash
python -m pytest -v
```
