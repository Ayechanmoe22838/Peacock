import pytest
from app.core.encryption import encrypt_data, decrypt_data, generate_blind_index

def test_encryption_decryption_cycle():
    raw_phone = "09450012345"
    encrypted = encrypt_data(raw_phone)
    assert encrypted != raw_phone
    assert encrypted.startswith("gAAAAA")

    decrypted = decrypt_data(encrypted)
    assert decrypted == raw_phone

def test_encryption_idempotence():
    raw_phone = "09790098765"
    encrypted1 = encrypt_data(raw_phone)
    # Double encrypting should recognize existing valid Fernet token and not double-wrap
    encrypted2 = encrypt_data(encrypted1)
    assert encrypted1 == encrypted2
    assert decrypt_data(encrypted2) == raw_phone

def test_decryption_fallback_on_plaintext():
    plain = "09123456789"
    # Fallback to plain text if token is not valid ciphertext
    result = decrypt_data(plain)
    assert result == plain

def test_blind_index_consistency():
    phone = "09450012345"
    idx1 = generate_blind_index(phone)
    idx2 = generate_blind_index(phone)
    assert idx1 == idx2
    assert len(idx1) == 64  # SHA256 hex string
