# PEACOCK – System Requirements

## 1. Functional Requirements (FR)

### FR-01: Authentication & Authorization
- Secure Argon2/bcrypt password hashing.
- Role-Based Access Control (RBAC) separating `admin` and `customer` roles.
- HTTP-only session cookies with configurable TTL and auto-redirect on session expiry.
- Ownership checks preventing customers from viewing or modifying other accounts' bookings or payments.

### FR-02: Public Browsing & Real-Time Availability
- Public catalog of active wedding venues with capacities, starting prices, and photo galleries.
- Instant AJAX-powered date and time availability checker.
- Curated wedding packages with transparent lists of included luxury services.
- Verified vendor showcase (Photography, Cinematography, Florists, Decoration, DJ, MC, Makeup).

### FR-03: Booking Management & Conflict Prevention
- Multi-step customer booking wizard linking venues, packages, and custom requirements.
- Automatic booking cost calculation (Venue Base Price + Package Price + Vendor Add-ons + Catering Portions).
- State-machine workflow: `Pending` -> `Approved` / `Rejected` -> `Confirmed` -> `Completed` / `Cancelled`.
- Concurrent transaction locking preventing overlapping confirmed bookings for any venue.

### FR-04: Digital Invitations & Public RSVP
- 13 distinct royal card designs extracted from authentic wedding stationery.
- Custom shareable invitation URLs (`/invitation/{token}`) with live view counting.
- Public RSVP submission capturing attending status, plus-ones, and dietary restrictions.

### FR-05: Seating Arrangements
- Interactive table creator with capacity enforcement.
- Duplicate seat assignment prevention.
- Real-time seating counter comparing total seated guests against table limits.

### FR-06: Budget & Expense Tracking
- Dynamic budget tracking comparing total allocated funds, estimated costs, and actual verified spend.
- Automated remaining balance calculation.
- Categorized expense logging (Venue, Package, Vendors, Attire, Miscellaneous).

### FR-07: KBZPay (KPay) Payment Processing
- Display of official KBZPay merchant credentials and instructions.
- Receipt screenshot upload with transaction ID logging.
- Admin verification queue: `Pending Verification` -> `Verified` (recalculates paid amount and balance) or `Rejected`.

### FR-08: Administrative Reporting & Exports
- Real-time revenue and booking status distribution charts via Chart.js.
- One-click CSV exports for bookings, customers, and payments.
- Server-rendered printable PDF management reports with official headers and timestamps via ReportLab.

---

## 2. Non-Functional Requirements (NFR)
- **NFR-01 Performance:** API p95 response time < 200ms on core database routes.
- **NFR-02 Page Speed:** Initial DOM load < 2.0s with optimized assets.
- **NFR-03 Security:** Authenticated Fernet encryption for all customer and guest phone numbers.
- **NFR-04 Usability:** WCAG 2.1 AA compliant color contrast (minimum 4.5:1 ratio) in both light and dark modes.
- **NFR-05 Browser Support:** Google Chrome, Microsoft Edge, Mozilla Firefox, Apple Safari.
- **NFR-06 Dual Theme Engine:** Instant theme switching between Light Mode, Dark Mode, and System Default with zero-flash rendering and persistence in `localStorage`.
