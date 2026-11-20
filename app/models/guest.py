from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Guest(Base):
    __tablename__ = "guests"

    guest_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    guest_name = Column(String(100), nullable=False, index=True)
    phone = Column(String(255), nullable=True)
    email = Column(String(120), nullable=True)
    category = Column(String(50), default="Friends", nullable=False)  # Bride Family, Groom Family, Close Friends, Colleagues, VIP, Relatives
    rsvp_status = Column(String(20), default="Pending", nullable=False)  # Pending, Accepted, Declined
    dietary_requirements = Column(String(255), nullable=True)
    plus_ones = Column(Integer, default=0, nullable=False)
    notes = Column(Text, nullable=True)
    invitation_token = Column(String(64), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    @property
    def plain_phone(self) -> str:
        from app.core.encryption import decrypt_data
        return decrypt_data(self.phone) if self.phone else ""

    booking = relationship("Booking", back_populates="guests")
    seating_assignment = relationship("SeatingAssignment", back_populates="guest", uselist=False, cascade="all, delete-orphan")
