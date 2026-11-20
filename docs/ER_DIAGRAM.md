# PEACOCK – Entity Relationship Diagram

The following Mermaid diagram visualizes the relational architecture of the Peacock platform across all 22 core tables.

```mermaid
erDiagram
    users ||--o{ bookings : "places"
    users ||--o{ notifications : "receives"
    users ||--o{ feedbacks : "submits"
    users ||--o{ audit_logs : "triggers"
    users ||--o{ payments : "verifies (admin)"

    venues ||--o{ venue_images : "contains"
    venues ||--o{ venue_availabilities : "locks"
    venues ||--o{ bookings : "hosts"

    packages ||--o{ package_services : "includes"
    packages ||--o{ bookings : "selected in"

    bookings ||--o{ booking_vendors : "contracts"
    vendors ||--o{ booking_vendors : "assigned"

    bookings ||--o{ booking_menus : "orders"
    menus ||--o{ booking_menus : "served in"

    bookings ||--o{ guests : "invites"
    bookings ||--o{ reception_tables : "configures"
    bookings ||--|| invitations : "designs"
    bookings ||--|| budgets : "allocates"
    bookings ||--o{ payments : "financed by"
    bookings ||--o{ event_schedules : "schedules"
    bookings ||--o{ feedbacks : "reviewed in"

    reception_tables ||--o{ seating_assignments : "has seats"
    guests ||--o| seating_assignments : "seated at"

    budgets ||--o{ expenses : "logs"
```

## Entity Cardinalities Summary
- **1-to-Many:** `users` -> `bookings`, `venues` -> `venue_images`, `packages` -> `package_services`, `bookings` -> `guests`, `bookings` -> `reception_tables`, `budgets` -> `expenses`, `bookings` -> `payments`, `bookings` -> `event_schedules`.
- **Many-to-Many (via junction):** `bookings` <-> `vendors` (via `booking_vendors`), `bookings` <-> `menus` (via `booking_menus`), `reception_tables` <-> `guests` (via `seating_assignments`).
- **1-to-1:** `bookings` <-> `invitations`, `bookings` <-> `budgets`.
