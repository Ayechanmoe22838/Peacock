# PEACOCK – API Documentation

## 1. Authentication Endpoints

### POST `/login`
- **Description:** Authenticates user credentials, sets secure HTTP-only JWT cookie.
- **Form Parameters:**
  - `email` (string, required)
  - `password` (string, required)
  - `next` (string, optional redirect path)
- **Responses:**
  - `303 See Other` -> Redirects to `/admin/dashboard` or `/customer/dashboard`.
  - `200 OK` -> Rerenders with error message on bad credentials.

### POST `/register`
- **Description:** Registers a new wedding customer account with encrypted phone storage.
- **Form Parameters:**
  - `full_name`, `email`, `phone`, `password`, `confirm_password`, `address`
- **Responses:**
  - `303 See Other` -> Redirects to login on success.
  - `200 OK` -> Validation error.

### GET `/logout`
- **Description:** Clears session cookie and redirects to `/login`.

---

## 2. Public Endpoints

### GET `/api/venues/{venue_id}/check-availability`
- **Description:** Real-time date and time slot availability check.
- **Query Parameters:**
  - `date` (`YYYY-MM-DD`)
  - `start_time` (`HH:MM`)
  - `end_time` (`HH:MM`)
- **Response Example:**
  ```json
  {
    "available": true,
    "reason": "Date and time slot available."
  }
  ```

### POST `/api/invitations/{token}/rsvp`
- **Description:** Public guest RSVP submission.
- **Payload:**
  ```json
  {
    "guest_name": "Ko Sithu Aung",
    "phone": "09781122334",
    "rsvp_status": "Accepted",
    "plus_ones": 1,
    "dietary_requirements": "Vegetarian",
    "notes": "Looking forward to celebrating!"
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "message": "RSVP recorded successfully."
  }
  ```

---

## 3. Administrative Endpoints

### POST `/admin/bookings/{id}/status`
- **Description:** Approves, confirms, or rejects a customer booking.
- **Form Parameters:**
  - `action`: `approve`, `confirm`, `reject`, `cancel`
  - `reason`: string (required if rejecting or cancelling)

### POST `/admin/payments/{id}/verify`
- **Description:** Verifies or rejects submitted KBZPay receipt.
- **Form Parameters:**
  - `action`: `approve` or `reject`
  - `admin_notes`: string (e.g. "Verified with KBZ merchant log.")

### GET `/admin/reports/export/bookings`
- **Query Parameter:** `format=csv` or `format=pdf`
- **Response:** Streaming CSV or binary PDF document with headers.
