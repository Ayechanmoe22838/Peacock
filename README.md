# PEACOCK – Smart Wedding Reception Management System

**PEACOCK** is a complete, production-ready, database-driven web application designed for luxury wedding reception planning and event management in Myanmar. Built using **Python FastAPI, MySQL 8.x, SQLAlchemy ORM, Alembic, HTML5, CSS3, JavaScript, Bootstrap 5, and Jinja2**, Peacock delivers an end-to-end management experience for wedding couples and venue administrators.

---

## 1. Technology Stack

- **Backend:** Python 3.14+, FastAPI, SQLAlchemy 2.0 ORM, PyMySQL, Alembic migrations, Pydantic Settings, Cryptography (Fernet AES authenticated encryption), bcrypt password hashing, python-jose, ReportLab (PDF export).
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Jinja2 Server-Side Templates, Bootstrap 5, Bootstrap Icons, Chart.js.
- **Database:** MySQL 8.x (`utf8mb4` encoding, InnoDB engine, strict decimal calculations for currency in MMK).
- **UI/UX Design:** Tailored using `ui-ux-pro-max-skill` adhering strictly to the official Peacock brand palette:
  - **Royal Peacock Blue:** `#063B78`
  - **Emerald Green:** `#006B45`
  - **Champagne Gold:** `#D6B875`
  - **Peacock Feather Gold:** `#C5A76B`
  - **Dark Emerald (Dark Mode Surface):** `#003B36`
  - **Dark Peacock Green (Dark Background):** `#102D28`
  - **Ivory:** `#FFFDF8` & **Warm Cream:** `#F8F3EA`
- **Testing:** Automated Pytest suite (29 tests, 100% pass rate).

---

## 2. Core Functional Modules

### Public Portal
- **Home Page:** Hero banner, quick stats, featured venues, luxury wedding packages, vendor showcase, how it works, and authentic verified customer testimonials.
- **Venues Catalog & Details:** High-resolution venue hall photography, capacity badges, rental pricing, included amenities, and an instant AJAX date/time availability checker.
- **Wedding Packages:** Multi-tier package options with itemized inclusions.
- **Vendors & Services:** Photography, cinematography, floral, decor, entertainment, makeup, and master of ceremonies.
- **Digital Invitation View & Live RSVP (`/invitation/{token}`):** Publicly shareable wedding invitation with real-time RSVP submission capturing attendance, plus-ones, and dietary restrictions.

### Customer Portal
- **Dashboard Overview:** Wedding countdown timer, venue and package summaries, budget spend percentage, guest RSVP tally, seating stats, timeline milestones, and notification alerts.
- **Profile Management:** Contact details with automatic Fernet phone encryption/decryption, mailing address, and secure password changes.
- **Booking Management & Wizard:** Multi-step booking workflow with real-time venue conflict prevention and financial calculation.
- **Digital Invitation Suite:** Interactive visual card selector featuring **13 exclusive stationery templates** (extracted from authentic wedding card designs) with live preview and shareable links.
- **Seating Planner:** Interactive banquet table manager with per-table guest capacity validation preventing overfilling.
- **Guest Management:** Comprehensive guest roster with RSVP tracking, plus-ones, and dietary preferences.
- **Budget & Expense Tracker:** Visual budget comparison (Total Budget vs. Estimated Cost vs. Actual Spend) with itemized expense logging.
- **KBZPay (KPay) Payment Processing:** Official merchant account display, receipt screenshot upload, and transaction reference tracking.
- **Event Schedule Timeline:** Chronological event milestones for the reception day.
- **Feedback & Reviews:** Post-wedding reviews submitted for admin moderation.

### Administrator Portal
- **Executive Dashboard:** Live database metrics (Total Customers, Venues, Bookings, Verified Revenue, Pending Bookings), Chart.js Monthly Revenue Trends, and Booking Status Distributions.
- **User Management:** Customer account overview with decrypted telephone viewing for authorized administrators.
- **Booking Management:** Complete booking review, cost breakdown inspection, approval, confirmation, and documented rejection workflows with automated customer notifications.
- **Payment Verification:** Inspection of uploaded KBZPay transaction slips, balance auto-reconciliation (`paid_amount` and `balance_amount`), and rejection with feedback.
- **Venue Blackout Date Manager:** Block dates for maintenance, private functions, or public holidays.
- **Catalog CRUD:** Venues, packages, vendors, and catering menus (Myanmar and International dishes).
- **Reports & Data Export:** Filterable booking and transaction summaries with one-click **CSV** and styled **PDF** export using ReportLab.
- **Audit Logs:** Immutable audit log trail recording financial actions, booking status changes, and user authentication events.

---

## 3. Dual-Theme Engine (Light, Dark, System Default)

The application provides a zero-flash, application-wide theme switching system:
- **Light Mode (`bi-sun`):** Elegant Ivory paper backgrounds, Champagne Gold accents, and Royal Peacock Blue highlights.
- **Dark Mode (`bi-moon-stars`):** Deep Emerald (`#003B36`), Dark Peacock Green (`#102D28`), and Dark Surface (`#183B35`) with Champagne Gold highlights and Light Ivory text.
- **System Default (`bi-display`):** Automatically detects OS preference and responds dynamically to changes.
- **Persistence:** Selected preference stored in `localStorage` and applied instantly before DOM render to prevent theme flashing.
- **Chart.js Integration:** Charts dynamically repaint labels, tooltips, and grid lines to match the active theme.

---

## 4. Default Seeded Accounts

| Role | Email | Password | Details |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@peacock.com` | `AdminPassword123!` | Complete administrative access to all platform controls |
| **Customer 1** | `customer@peacock.com` | `CustomerPassword123!` | **Cherry** (Confirmed booking `BK-202611-001`, Grand Ballroom) |
| **Customer 2** | `thura@gmail.com` | `CustomerPassword123!` | Thura Aung (Pending booking request `BK-202611-002`) |
| **Customer 3** | `maythu@gmail.com` | `CustomerPassword123!` | May Thu Zin (Completed booking `BK-202610-003` with public review) |

---

## 5. Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.14.3)
- MySQL 8.0+ running locally on `127.0.0.1:3306`

### 2. Configuration (`.env`)
Verify `.env` in the project root:
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

### 3. Database Migrations & Seeding
```bash
# Apply database migrations
alembic upgrade head

# Seed demo data (Venues, packages, vendors, menus, invitations, bookings)
python scripts/seed_data.py
```

### 4. Start Application
```bash
# Using Uvicorn directly
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Or via the runner script
python run.py
```
Open your browser to: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 6. Running Automated Tests

Run the full pytest suite:
```bash
python -m pytest -v
```
All 39 tests validate RBAC guards, booking conflict prevention, Fernet phone encryption/decryption, budget calculations, payment verification workflows, public digital invitation views across 13 stationery templates, seating constraints, catering portion selections, high-contrast black/white theme compliance, Table 8.2 color tokens, and PDF/CSV report generation.

---

## 7. Documentation Suite
Detailed technical documentation (all 18 required documents) is available in the `docs/` directory:
1. [Project Overview](docs/PROJECT_OVERVIEW.md)
2. [Requirements](docs/REQUIREMENTS.md)
3. [User Roles and Permissions Matrix](docs/USER_ROLES_AND_PERMISSIONS.md)
4. [System Architecture](docs/SYSTEM_ARCHITECTURE.md)
5. [Database Design](docs/DATABASE_DESIGN.md)
6. [ER Diagram](docs/ER_DIAGRAM.md)
7. [Use Case Diagram](docs/USE_CASE_DIAGRAM.md)
8. [Activity Diagrams](docs/ACTIVITY_DIAGRAMS.md)
9. [Sequence Diagrams](docs/SEQUENCE_DIAGRAMS.md)
10. [API Documentation](docs/API_DOCUMENTATION.md)
11. [Installation Guide](docs/INSTALLATION_GUIDE.md)
12. [Configuration Guide](docs/CONFIGURATION_GUIDE.md)
13. [Customer User Manual](docs/USER_MANUAL.md)
14. [Administrator Manual](docs/ADMIN_MANUAL.md)
15. [Testing Report](docs/TESTING_REPORT.md)
16. [Security Documentation](docs/SECURITY_DOCUMENTATION.md)
17. [Known Limitations](docs/KNOWN_LIMITATIONS.md)
18. [Future Enhancements](docs/FUTURE_ENHANCEMENTS.md)
- [Stage Development Log (Stages 1-11)](docs/STAGE_DEVELOPMENT_LOG.md)
- [Progress Log](docs/progress_log.md)
