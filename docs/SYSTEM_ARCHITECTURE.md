# PEACOCK – System Architecture

## 1. Architectural Overview
Peacock is built as a modular, database-driven web application using Python FastAPI, SQLAlchemy ORM, and MySQL 8.x. The architecture adheres to clean separation of concerns, dividing business logic, data persistence, HTTP routing, security enforcement, and presentation into decoupled layers.

```
+-------------------------------------------------------------------------+
|                        Browser Client (HTML5 / CSS3 / JS)               |
|            Bootstrap 5, Chart.js, Bootstrap Icons, Theme Engine         |
+-------------------------------------------------------------------------+
                                    |  HTTP / Cookie Auth
                                    v
+-------------------------------------------------------------------------+
|                      FastAPI Application Gateway                        |
|  - CORS Middleware      - Static & Media Mounters   - Exception Handler |
+-------------------------------------------------------------------------+
                                    |
          +-------------------------+-------------------------+
          |                         |                         |
          v                         v                         v
+-------------------+     +-------------------+     +-------------------+
|  Public Router    |     |  Customer Router  |     |   Admin Router    |
| - Home, Venues    |     | - Wizard, Profile |     | - Dashboard       |
| - Packages, About |     | - Budget, Seating |     | - User Management |
| - Digital RSVP    |     | - Invitations     |     | - Payment Review  |
+-------------------+     +-------------------+     +-------------------+
          |                         |                         |
          +-------------------------+-------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                              Service Layer                              |
|  - booking_service.py     - payment_service.py     - budget_service.py  |
|  - report_service.py      - encryption_service.py  - notification_svc.py|
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                       Data Access Layer (SQLAlchemy ORM)                |
|  22 Normalized Entities: Users, Venues, Packages, Bookings, Payments... |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                             MySQL 8.x Database                          |
|         InnoDB Engine, ACID Transactions, Foreign Key Constraints       |
+-------------------------------------------------------------------------+
```

## 2. Directory Structure
```
d:\PEACOCK(Smart Wedding Reception Management System)\
├── app/
│   ├── main.py                  # Application entry point and router inclusion
│   ├── core/
│   │   ├── config.py            # Pydantic BaseSettings environment configuration
│   │   ├── database.py          # SQLAlchemy SessionLocal, engine, and get_db dependency
│   │   ├── encryption.py        # Fernet AES authenticated encryption & blind indexing
│   │   ├── invitation_templates.py # Digital card template catalog
│   │   ├── permissions.py       # RBAC dependency guards (admin, customer, guest)
│   │   ├── security.py          # Password hashing and JWT session tokens
│   │   └── templates.py         # Jinja2 template environment and custom filters
│   ├── models/                  # 22 Normalized SQLAlchemy ORM Models
│   ├── schemas/                 # Pydantic request and response schemas
│   ├── routers/                 # Modular HTTP route controllers
│   ├── services/                # Reusable business logic services
│   ├── static/                  # CSS tokens, vanilla JS, images, fonts
│   └── templates/               # Jinja2 HTML templates
├── alembic/                     # Database migration management
├── docs/                        # Complete technical and operational documentation
├── media/                       # Protected uploaded receipts and user media
├── scripts/                     # Database seeding and utility scripts
├── tests/                       # Pytest automated test suite
├── requirements.txt             # Verified Python dependencies
├── alembic.ini                  # Alembic database configuration
└── run.py                       # Local startup runner script
```
