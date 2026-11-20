from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)
    role = Column(String(20), nullable=False, default="customer")  # 'admin' or 'customer'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @property
    def plain_phone(self) -> str:
        from app.core.encryption import decrypt_data
        return decrypt_data(self.phone) if self.phone else ""

    # Relationships
    bookings = relationship("Booking", back_populates="customer", cascade="all, delete-orphan", foreign_keys="Booking.customer_id")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="customer", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
