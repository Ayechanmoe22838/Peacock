from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vendor_name = Column(String(150), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # Photography, Videography, Decoration, Florist, Entertainment, Makeup Artist, Master of Ceremonies, Music/DJ
    description = Column(Text, nullable=True)
    contact_name = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=False)
    email = Column(String(120), nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    image_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking_associations = relationship("BookingVendor", back_populates="vendor", cascade="all, delete-orphan")

class BookingVendor(Base):
    __tablename__ = "booking_vendors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.vendor_id", ondelete="CASCADE"), nullable=False)
    price_agreed = Column(Numeric(12, 2), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="booking_vendors")
    vendor = relationship("Vendor", back_populates="booking_associations")
