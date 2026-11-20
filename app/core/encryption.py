import base64
import hashlib
import hmac
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings

def _get_fernet_key() -> bytes:
    """
    Derives a 32-byte urlsafe base64 key from SECRET_KEY.
    """
    key_material = settings.SECRET_KEY.encode("utf-8")
    return base64.urlsafe_b64encode(hashlib.sha256(key_material).digest())

def encrypt_data(plaintext: Optional[str]) -> Optional[str]:
    """
    Encrypts string using authenticated Fernet encryption.
    """
    if not plaintext:
        return plaintext
    # If already a valid Fernet token, do not double-encrypt
    if plaintext.startswith("gAAAAA"):
        try:
            f = Fernet(_get_fernet_key())
            f.decrypt(plaintext.encode("utf-8"))
            return plaintext
        except Exception:
            pass
    f = Fernet(_get_fernet_key())
    return f.encrypt(plaintext.encode("utf-8")).decode("utf-8")

def decrypt_data(ciphertext: Optional[str]) -> Optional[str]:
    """
    Decrypts string using authenticated Fernet encryption.
    Falls back gracefully if the data was not encrypted (plaintext).
    """
    if not ciphertext:
        return ciphertext
    try:
        f = Fernet(_get_fernet_key())
        return f.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
    except (InvalidToken, Exception):
        # Plaintext fallback for legacy/unencrypted data
        return ciphertext

def generate_blind_index(value: str) -> str:
    """
    Generates a keyed blind index using HMAC-SHA256 for exact match searching
    without exposing plaintext or storing reversible deterministic hashes.
    """
    if not value:
        return ""
    key = hashlib.sha256(settings.SECRET_KEY.encode("utf-8") + b":blind_index").digest()
    return hmac.new(key, value.strip().encode("utf-8"), hashlib.sha256).hexdigest()
