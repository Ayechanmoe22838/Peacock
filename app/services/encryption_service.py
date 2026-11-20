from typing import Optional
from app.core.encryption import encrypt_data, decrypt_data, generate_blind_index

class EncryptionService:
    @staticmethod
    def encrypt_phone(phone: Optional[str]) -> Optional[str]:
        return encrypt_data(phone)

    @staticmethod
    def decrypt_phone(encrypted_phone: Optional[str]) -> Optional[str]:
        return decrypt_data(encrypted_phone)

    @staticmethod
    def get_search_index(phone: str) -> str:
        return generate_blind_index(phone)

encryption_service = EncryptionService()
