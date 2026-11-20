# USER ROLES AND PERMISSIONS MATRIX
# PEACOCK – Smart Wedding Reception Management System

---

## 1. Overview & Security Model

The **PEACOCK** application implements strict, server-side **Role-Based Access Control (RBAC)** across all HTTP endpoints and domain operations. Authorization is never delegated to the client; all state transitions and protected resources verify user authentication, role assignment, and resource ownership before executing queries.

Two primary roles exist within the system:
1. **Administrator (`admin`)**: Manages the overarching platform, venues, wedding packages, master service vendors, catering culinary items, blackouts/availability locks, booking approvals, payment receipt verification, financial audit logs, and reports.
2. **Wedding Customer (`customer`)**: Plans and configures their individual wedding reception, manages personal profiles, browses catalogs, submits booking requests, arranges banquet seating, compiles guest rosters, manages wedding budgets, submits KBZPay transaction references, and designs shareable digital invitation suites.

---

## 2. Role-Based Access Control (RBAC) Matrix

| Module / Operation | Public (Guest) | Customer (`customer`) | Administrator (`admin`) |
| :--- | :---: | :---: | :---: |
| **Public Website Browsing** (Home, About, Venues, Packages, Services, Contact) | ✅ Allowed | ✅ Allowed | ✅ Allowed |
| **Theme Switching** (Light Mode / Dark Mode / System Default) | ✅ Allowed | ✅ Allowed | ✅ Allowed |
| **Customer Registration & Login** | ✅ Allowed | ✅ Logged In | ✅ Logged In |
| **Password Reset Workflow** | ✅ Allowed | ✅ Allowed | ✅ Allowed |
| **Customer Profile Management** (Decrypted view, update, password change) | ❌ Denied | ✅ Own Profile Only | ❌ Use Admin Profile |
| **Decrypted Phone Access** | ❌ Denied | ✅ Own Phone Only | ✅ Authorized Admin Audit |
| **Submit New Booking Request** | ❌ Denied (Redirect) | ✅ Allowed | ❌ Denied (Customer Role Only) |
| **View Booking History** | ❌ Denied | ✅ Own Bookings Only | ✅ All Customer Bookings |
| **Booking Approval / Rejection** | ❌ Denied | ❌ Denied | ✅ Allowed (With audit trail) |
| **Booking Cancellation Request** | ❌ Denied | ✅ Own Bookings | ✅ Direct Process |
| **Venue Blackout Date Scheduling** | ❌ Denied | ❌ Denied | ✅ Allowed |
| **Catalog Management** (Venues, Packages, Vendors, Menus CRUD) | ❌ Denied | ❌ Denied | ✅ Allowed |
| **Select & Add Catering Portions to Booking** | ❌ Denied | ✅ Own Booking Only | ❌ Denied |
| **Banquet Seating Management** (Tables, Guest Seat Assignments) | ❌ Denied | ✅ Own Booking Only | ❌ Denied |
| **Guest List Management** (Add, Delete, RSVP Tracking) | ❌ Denied | ✅ Own Booking Only | ❌ Read-Only Audit |
| **Digital Invitation Studio** (Choose from 13 designs, live preview) | ❌ Denied | ✅ Own Booking Only | ❌ Denied |
| **Public Shareable Invitation & RSVP** (`/invitation/{token}`) | ✅ Allowed | ✅ Allowed | ✅ Allowed |
| **Wedding Budget & Expense Logging** | ❌ Denied | ✅ Own Booking Only | ❌ Denied |
| **KBZPay Payment Submission** (Ref ID, receipt upload) | ❌ Denied | ✅ Own Booking Only | ❌ Denied |
| **Payment Verification & Approval** (Inspect receipt, credit balance) | ❌ Denied | ❌ Denied | ✅ Allowed |
| **Event Day Schedule Timeline** | ❌ Denied | ✅ Own Booking Only | ❌ Denied |
| **Notifications** (Receive and mark read) | ❌ Denied | ✅ Own Alerts | ✅ System Announcements |
| **Customer Feedback Submission** | ❌ Denied | ✅ Eligible Completed Bookings Only | ❌ Denied |
| **Customer Feedback Moderation** | ❌ Denied | ❌ Denied | ✅ Allowed |
| **Business Analytics & PDF/CSV Reports** | ❌ Denied | ❌ Denied | ✅ Allowed |
| **Audit Log Trail** | ❌ Denied | ❌ Denied | ✅ Read-Only (Immutable) |

---

## 3. Customer Ownership & Data Isolation

To prevent **Insecure Direct Object Reference (IDOR)** vulnerabilities:
- Each database operation verifying a booking (`booking_id`), budget (`budget_id`), guest (`guest_id`), table (`table_id`), or invitation (`invitation_id`) checks that `booking.customer_id == current_user.user_id`.
- Attempts to query or mutate records belonging to another customer result in immediate `403 Forbidden` or `404 Not Found` responses.
- Customer passwords use bcrypt hashing with salted work factor of 12.
- Telephone numbers are encrypted at rest with Fernet symmetric AES-CBC encryption using a secure server key.
