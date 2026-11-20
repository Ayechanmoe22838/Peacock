from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    payment_reference = Column(String(50), unique=True, index=True, nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(50), default="KBZPay", nullable=False)  # KBZPay, Bank Transfer, Cash Deposit, WavePay
    transaction_reference = Column(String(100), nullable=False, index=True)
    receipt_image = Column(String(255), nullable=True)
    payment_status = Column(String(30), default="Pending Verification", index=True, nullable=False)  # Pending, Pending Verification, Verified, Rejected, Refunded
    notes = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    verified_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="payments")
    verifier = relationship("User", foreign_keys=[verified_by])
