# SEQUENCE DIAGRAMS
# PEACOCK – Smart Wedding Reception Management System

---

## 1. Booking Creation with Real-Time Conflict Check

The sequence diagram below shows the interaction between the Customer Browser, FastAPI Booking Router, Database Engine, and Notification Service when submitting a new wedding reservation.

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Customer (Cherry)
    participant UI as Browser / Frontend
    participant Router as Bookings Router (FastAPI)
    participant DB as MySQL Database
    participant Notif as Notification Service

    Customer->>UI: Selects Venue, Date (2027-02-14), 17:00-22:00, Package
    Customer->>UI: Clicks "Submit Booking Request"
    UI->>Router: POST /customer/booking/wizard (FormData)
    
    activate Router
    Note over Router: Check customer authentication & session
    
    Router->>DB: SELECT * FROM venue_availabilities WHERE venue_id = ? AND date = ? AND is_available = False
    DB-->>Router: No blackout record found
    
    Router->>DB: SELECT * FROM bookings WHERE venue_id = ? AND event_date = ? AND booking_status = 'Confirmed'
    DB-->>Router: No overlapping confirmed booking
    
    Note over Router: Server-side cost calculation: Venue + Package + Services
    
    Router->>DB: INSERT INTO bookings (booking_reference, customer_id, venue_id, costs, status='Pending')
    DB-->>Router: booking_id: 20
    
    Router->>DB: INSERT INTO budgets (booking_id, total_budget, estimated_cost)
    DB-->>Router: budget_id: 15
    
    Router->>Notif: create_notification(admin_id, "New Booking BK-2027-...", "booking")
    Notif->>DB: INSERT INTO notifications
    
    Router-->>UI: 303 Redirect -> /customer/bookings/20 (Success)
    deactivate Router
    
    UI-->>Customer: Display booking details with "Pending" badge
```

---

## 2. KBZPay Payment Verification & Balance Settlement

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Customer (Cherry)
    actor Admin as Peacock Administrator
    participant UI as Admin Dashboard
    participant Router as Admin Router (FastAPI)
    participant DB as MySQL Database
    participant Audit as Audit Service
    participant Notif as Notification Service

    Customer->>Router: POST /customer/payments/submit (KPay Ref: 0202611162391024, Slip: receipt.jpg)
    Router->>DB: INSERT INTO payments (status='Pending Verification')
    
    Admin->>UI: Opens /admin/payments
    UI->>Router: GET /admin/payments
    Router->>DB: SELECT * FROM payments WHERE payment_status = 'Pending Verification'
    DB-->>UI: List payments with slip thumbnail & transaction ID
    
    Admin->>UI: Checks merchant bank portal, clicks "Approve"
    UI->>Router: POST /admin/payments/{id}/verify (action='approve')
    
    activate Router
    Router->>DB: UPDATE payments SET payment_status='Verified', verified_at=NOW()
    Router->>DB: UPDATE bookings SET paid_amount = paid_amount + ?, balance_amount = total_cost - paid_amount
    Router->>DB: UPDATE bookings SET booking_status='Confirmed' WHERE booking_status='Approved'
    
    Router->>Audit: log_action(admin_id, "PAYMENT_VERIFIED", payment_id, details)
    Audit->>DB: INSERT INTO audit_logs
    
    Router->>Notif: create_notification(customer_id, "Payment Verified. Booking Confirmed!", "payment")
    Notif->>DB: INSERT INTO notifications
    
    Router-->>UI: 303 Redirect -> /admin/payments (Success alert)
    deactivate Router
    
    UI-->>Admin: Table updates with "Verified" badge
```

---

## 3. Digital Invitation & Guest RSVP Submission

```mermaid
sequenceDiagram
    autonumber
    actor Guest as Wedding Guest (e.g. Min Thant)
    participant Browser as Guest Mobile Browser
    participant App as Public Router (FastAPI)
    participant DB as MySQL Database

    Guest->>Browser: Opens /invitation/peacock-acm-minthant-2026
    Browser->>App: GET /invitation/{token}
    
    activate App
    App->>DB: SELECT * FROM invitations WHERE shareable_token = ?
    DB-->>App: Invitation details, template_name='royal_rose'
    
    App->>DB: UPDATE invitations SET views_count = views_count + 1 WHERE invitation_id = ?
    
    App-->>Browser: 200 OK (Renders luxury stationery card & RSVP form)
    deactivate App
    
    Guest->>Browser: Fills RSVP: Name="Min Thant", Phone="09420011223", RSVP="Accepted", Plus-Ones=1, Dietary="No Peanuts"
    Guest->>Browser: Clicks "Submit RSVP"
    
    Browser->>App: POST /invitation/{token}/rsvp (JSON Payload)
    activate App
    App->>DB: INSERT INTO guests (booking_id, guest_name, phone, rsvp_status='Accepted', plus_ones=1, dietary=...)
    DB-->>App: guest_id: 42
    
    App-->>Browser: JSON {"success": true, "message": "RSVP recorded with gratitude."}
    deactivate App
    
    Browser-->>Guest: Shows elegant confirmation modal & celebration confetti
```
