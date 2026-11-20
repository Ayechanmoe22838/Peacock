from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

class EventSchedule(Base):
    __tablename__ = "event_schedules"

    schedule_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    activity_name = Column(String(150), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="schedules")
