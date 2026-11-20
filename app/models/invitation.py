from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

class Invitation(Base):
    __tablename__ = "invitations"

    invitation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), unique=True, nullable=False)
    template_name = Column(String(50), default="classic_gold", nullable=False)  # classic_gold, royal_rose, sage_elegance, modern_minimal
    custom_title = Column(String(200), nullable=False)
    custom_message = Column(Text, nullable=False)
    wedding_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    venue_name = Column(String(150), nullable=False)
    venue_address = Column(String(255), nullable=False)
    shareable_token = Column(String(64), unique=True, index=True, nullable=False)
    views_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="invitation")
