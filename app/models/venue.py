from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    venue_name = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    base_price = Column(Numeric(12, 2), nullable=False)
    facilities = Column(Text, nullable=True)
    status = Column(String(20), default="active", nullable=False)  # 'active', 'maintenance', 'inactive'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    images = relationship("VenueImage", back_populates="venue", cascade="all, delete-orphan", order_by="VenueImage.is_primary.desc()")
    availabilities = relationship("VenueAvailability", back_populates="venue", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="venue")

class VenueImage(Base):
    __tablename__ = "venue_images"

    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    venue_id = Column(Integer, ForeignKey("venues.venue_id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    caption = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    venue = relationship("Venue", back_populates="images")

class VenueAvailability(Base):
    __tablename__ = "venue_availabilities"

    availability_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    venue_id = Column(Integer, ForeignKey("venues.venue_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    is_available = Column(Boolean, default=True, nullable=False)
    reason = Column(String(255), nullable=True)
    operating_hours = Column(String(100), default="08:00 - 22:00", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    venue = relationship("Venue", back_populates="availabilities")
