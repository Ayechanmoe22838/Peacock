# Phase 3 Summary: Core Services, Security Architecture & Business Logic

## Date & Time
2026-11-18T11:45:00+06:30

## Objectives
1. Implement core business services ensuring strict business rules (double-booking prevention, exact decimal currency operations in Myanmar Kyat, safe KPay manual verification workflow).
2. Establish robust Authentication and Role-Based Access Control (RBAC) with HTTP-only secure cookie support and seamless browser redirection.
3. Build reporting services supporting CSV data streaming and styled PDF exports using ReportLab.
4. Establish unified template rendering conforming to Starlette 1.6 / FastAPI standards.

## Architecture & Implementation Details

### 1. Business Logic Services (`app/services/`)
- **Booking Service (`booking_service.py`)**:
  - `check_venue_availability(db, venue_id, event_date, start_time, end_time, exclude_booking_id)`: Enforces Rule 5 by verifying that no overlapping `Approved` or `Confirmed` booking exists for the same venue where `start_time < existing_end` and `end_time > existing_start`. Also checks `VenueAvailability` blackout dates.
  - `calculate_booking_cost(db, venue_id, package_id, guest_count, vendor_ids, menu_ids)`: Computes base venue price, package price, selected vendor prices, and menu per-person costs multiplied by guest count.
  - `create_wedding_booking(...)`: Handles end-to-end booking creation with unique booking references (`BK-YYYYMM-XXXXX`), initializes default budget (`BK-BUDGET-XXXXX`), and records initial audit log entry.
- **Payment Service (`payment_service.py`)**:
  - `submit_payment(...)`: Safely handles KBZPay (KPay) deposit and progress payment submissions. Generates reference `PAY-YYYYMM-XXXXX`, saves receipt image to `media/payment_receipts/`, and sets status to `Pending Verification`.
  - `verify_payment(...)`: Admin-only action to approve or reject submitted payments. Automatically synchronizes `booking.paid_amount` and `booking.balance_amount`, triggers customer notifications, and logs audit entries.
- **Budget Service (`budget_service.py`)**:
  - `recalculate_budget(...)`: Synchronizes total budget, itemized expenses, and remaining balance.
- **Report Service (`report_service.py`)**:
  - Generates streaming CSV reports for bookings and payments with complete transaction metadata.
  - Generates executive PDF documents using ReportLab `SimpleDocTemplate`, `Table`, `TableStyle`, and custom burgundy/champagne palettes matching the Peacock design system.
- **Notification Service (`notification_service.py`)**:
  - Dispatches persistent user notifications for booking confirmations, payment verifications, and reminders.

### 2. Security & RBAC (`app/core/`)
- **Security (`security.py`)**:
  - Secure password hashing and verification using `bcrypt`.
  - JWT token creation and decoding with configurable expiration.
- **Permissions (`permissions.py`)**:
  - `get_current_user`: Dual lookup via HTTP `Authorization: Bearer <token>` header or `access_token` cookie. Automatically redirects unauthenticated HTML requests to `/login?redirect=...`.
  - `get_current_admin`: Restricts access to users with `role == "admin"`.
  - `get_current_customer`: Restricts access to active users with `role == "customer"`.
- **Template Rendering Helper (`templates.py`)**:
  - `render_template(request, name, context, status_code)`: Adapts Starlette 1.6's explicit keyword signature `templates.TemplateResponse(request=request, name=name, context=ctx)` and automatically injects `request`, `settings`, and global context variables.

## Verification
- Unit tested password hashing and JWT encoding/decoding.
- Verified venue overlap validation with concurrent booking test fixtures.
- Verified payment verification recalculation with exact decimal arithmetic.
