# CONFIGURATION GUIDE
# PEACOCK – Smart Wedding Reception Management System

---

## 1. Environment Configuration (`.env`)

The application loads environment variables at startup via `pydantic-settings` from the `.env` file located in the project root directory.

### Environment Variables Reference

| Variable Name | Required | Default Value | Description |
| :--- | :---: | :--- | :--- |
| `PROJECT_NAME` | No | `Peacock – Smart Wedding Reception Management System` | Branding title displayed across website and emails |
| `SECRET_KEY` | **Yes** | *Set random string* | Cryptographic key used to sign JWT session cookies |
| `ALGORITHM` | No | `HS256` | JWT signature algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `1440` (24 hours) | Duration of authentication session cookie before expiration |
| `MYSQL_USER` | **Yes** | `root` | MySQL database username |
| `MYSQL_PASSWORD` | **Yes** | `root` | MySQL database password |
| `MYSQL_HOST` | **Yes** | `127.0.0.1` | MySQL server host address |
| `MYSQL_PORT` | No | `3306` | MySQL server port |
| `MYSQL_DB` | **Yes** | `peacock_db` | Target database name |
| `DATABASE_URL` | No | *Computed from above* | Full SQLAlchemy database connection string |
| `UPLOAD_DIR` | No | `media` | Local file system folder for receipt and image uploads |
| `CURRENCY_CODE` | No | `MMK` | ISO 4217 Currency Code for Myanmar Kyats |
| `CURRENCY_SYMBOL` | No | `Ks` | Display symbol for prices and statements |
| `FERNET_KEY` | No | *Optional override* | 32-byte Base64-encoded key for phone number encryption |
| `ADMIN_EMAIL` | No | `admin@peacock.com` | Default super-admin email seeded at startup |
| `ADMIN_PASSWORD` | No | `AdminPassword123!` | Initial admin password (change immediately after first login) |
| `ADMIN_NAME` | No | `Peacock Administrator` | Initial administrator display name |

---

## 2. Phone Number Encryption Configuration

In strict compliance with **Section 14.4** of `implementation.md`:
> *"Never store plain-text phone number in database. But it (phone number) shows in frontend website page, like 09984122721 or +959981485229."*

The application employs **Fernet authenticated encryption** (AES-128 in CBC mode with HMAC SHA-256):
- If `FERNET_KEY` is not provided in `.env`, the system automatically derives a deterministic, stable 32-byte key from `SECRET_KEY` using SHA-256 and Base64 URL encoding.
- This ensures existing encrypted phone numbers in `users` and `guests` tables decrypt seamlessly across server restarts without losing data.
- If you wish to rotate keys, generate a fresh key using Python:
  ```python
  from cryptography.fernet import Fernet
  print(Fernet.generate_key().decode())
  ```
  and assign it to `FERNET_KEY` in `.env`.

---

## 3. Database Migration Configuration (`alembic.ini`)

Alembic migrations are configured to connect to MySQL using the URL defined in `.env`:
- Migration scripts reside in `alembic/versions/`.
- To create a new migration after editing SQLAlchemy models in `app/models/`:
  ```bash
  alembic revision --autogenerate -m "add_new_columns"
  ```
- To apply migrations to MySQL:
  ```bash
  alembic upgrade head
  ```

---

## 4. Production Security Hardening

When deploying to a public cloud or production host:
1. Generate a 64-character random `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. Set `DEBUG=False` and disable Swagger API documentation if exposed publicly.
3. Configure reverse proxy (Nginx or Caddy) with SSL/TLS termination and enable `Secure=True` on cookies:
   ```python
   response.set_cookie(key="access_token", value=token, httponly=True, secure=True, samesite="lax")
   ```
4. Set strict file upload permissions on the `media/` folder preventing script execution.
