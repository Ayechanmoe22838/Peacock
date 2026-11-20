# PEACOCK – Database Design

## 1. Relational Database Principles
The database is deployed on **MySQL 8.x** utilizing the **InnoDB** storage engine to guarantee full ACID transaction safety, foreign key referential integrity, and row-level locking during booking operations.

### Key Database Conventions:
- **Currency:** Myanmar Kyat (`MMK`) stored strictly as `DECIMAL(12, 2)` to eliminate IEEE 754 floating-point rounding errors.
- **Timestamps:** UTC `created_at` and `updated_at` records across all core tables.
- **Data Privacy:** Customer and guest telephone numbers stored as 255-character Fernet authenticated ciphertext.

---

## 2. Database Entities & Tables (22 Models)

| Entity / Table | Primary Key | Key Foreign Keys | Purpose |
| :--- | :--- | :--- | :--- |
| `users` | `user_id` (INT) | None | System accounts (Admin & Customers) |
| `venues` | `venue_id` (INT) | None | Wedding reception venues & physical properties |
| `venue_images` | `image_id` (INT) | `venue_id` -> `venues` | Hall decoration and stage photography |
| `venue_availabilities` | `availability_id` (INT) | `venue_id` -> `venues` | Date blackouts and operational maintenance |
| `packages` | `package_id` (INT) | None | Curated wedding package offerings |
| `package_services` | `service_id` (INT) | `package_id` -> `packages` | Specific items included in packages |
| `bookings` | `booking_id` (INT) | `customer_id`, `venue_id`, `package_id` | Core wedding reservation records |
| `vendors` | `vendor_id` (INT) | None | Photography, floral, music, and MC vendors |
| `booking_vendors` | `id` (INT) | `booking_id`, `vendor_id` | Additional vendor services chosen for a booking |
| `menus` | `menu_id` (INT) | None | Catering banquet dishes (Myanmar & Intl) |
| `booking_menus` | `id` (INT) | `booking_id`, `menu_id` | Specific catering portions linked to a booking |
| `guests` | `guest_id` (INT) | `booking_id` -> `bookings` | Wedding guest list, RSVP, and dietary needs |
| `invitations` | `invitation_id` (INT) | `booking_id` -> `bookings` | Customized digital wedding card invitations |
| `reception_tables` | `table_id` (INT) | `booking_id` -> `bookings` | Physical banquet tables and capacities |
| `seating_assignments` | `assignment_id` (INT) | `table_id`, `guest_id` | Seat allocation per guest |
| `budgets` | `budget_id` (INT) | `booking_id` -> `bookings` | Financial budget plan and spend summary |
| `expenses` | `expense_id` (INT) | `budget_id` -> `budgets` | Itemized wedding expenditures |
| `payments` | `payment_id` (INT) | `booking_id`, `verified_by` | KBZPay deposits and transaction records |
| `event_schedules` | `schedule_id` (INT) | `booking_id` -> `bookings` | Reception timeline milestones |
| `notifications` | `notification_id` (INT) | `user_id` -> `users` | User alerts and booking status updates |
| `feedbacks` | `feedback_id` (INT) | `booking_id`, `customer_id` | Post-wedding customer reviews & ratings |
| `audit_logs` | `log_id` (INT) | `user_id` -> `users` | Security and administrative audit trail |
