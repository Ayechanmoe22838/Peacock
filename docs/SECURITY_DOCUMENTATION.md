# PEACOCK – Security & Privacy Documentation

## 1. Security Architecture Summary
Peacock implements end-to-end defense-in-depth protections tailored for wedding management and mobile financial workflows.

---

## 2. Authentication & Session Management
- **Password Hashing:** Passwords hashed with `bcrypt` (12-round salt).
- **Session Tokens:** Stateless JWT tokens signed with SHA-256 HMAC (`HS256`).
- **Cookie Security:**
  - `httponly=True`: Inaccessible to browser JavaScript, mitigating XSS token theft.
  - `samesite="lax"`: Mitigates Cross-Site Request Forgery (CSRF).
  - Explicit session expiration (default: 24 hours / 1440 minutes).

---

## 3. Customer Phone Number Encryption
In accordance with Section 14 of the master implementation instructions:
- **Algorithm:** Authenticated symmetric encryption using **Fernet (AES-128 in CBC mode with PKCS7 padding and HMAC-SHA256 authentication)**.
- **Key Derivation:** Cryptographic 32-byte key derived from `SECRET_KEY` via SHA-256.
- **Database Storage:** Stored as `VARCHAR(255)` containing base64url-encoded ciphertext.
- **In-Memory Decryption:** Phone numbers are only decrypted in authorized application memory when rendering profiles or guest rosters for authenticated users.
- **Blind Indexing:** Keyed HMAC-SHA256 blind indexing (`generate_blind_index`) is provided for constant-time exact match searches without exposing raw plaintext.

---

## 4. Role-Based Access Control (RBAC) & Isolation
- **Role Enforcement:** FastAPI dependencies `get_current_admin` and `get_current_customer` validate JWT claims before controller execution.
- **Data Isolation:** Customer queries are strictly filtered by `booking.customer_id == user.user_id`, preventing Insecure Direct Object References (IDOR).
- **Audit Logging:** Sensitive financial actions (e.g. `PAYMENT_VERIFIED`, `PAYMENT_REJECTED`) and state transitions (`BOOKING_APPROVED`, `BOOKING_REJECTED`) are recorded in the immutable `audit_logs` table.

---

## 5. Financial Transaction Safety
- **Decimal Precision:** All monetary amounts are handled using Python's `Decimal` type and MySQL `DECIMAL(12, 2)` columns, preventing rounding discrepancies.
- **Manual Verification Workflow:** KPay mobile wallet payments require explicit super administrator review of uploaded receipt screenshots before updating booking balances.
