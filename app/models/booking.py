from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_reference = Column(String(30), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.venue_id", ondelete="RESTRICT"), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.package_id", ondelete="SET NULL"), nullable=True)
    
    event_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    guest_count = Column(Integer, nullable=False)
    special_requirements = Column(Text, nullable=True)
    
    # Financial breakdown (in MMK)
    venue_cost = Column(Numeric(12, 2), default=0.00, nullable=False)
    package_cost = Column(Numeric(12, 2), default=0.00, nullable=False)
    vendors_cost = Column(Numeric(12, 2), default=0.00, nullable=False)
    catering_cost = Column(Numeric(12, 2), default=0.00, nullable=False)
    total_cost = Column(Numeric(12, 2), default=0.00, nullable=False)
    paid_amount = Column(Numeric(12, 2), default=0.00, nullable=False)
    balance_amount = Column(Numeric(12, 2), default=0.00, nullable=False)
    
    # Status lifecycle
    # Pending, Approved, Confirmed, Rejected, Cancellation Requested, Cancelled, Completed
    booking_status = Column(String(30), default="Pending", index=True, nullable=False)
    rejection_reason = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    customer = relationship("User", back_populates="bookings", foreign_keys=[customer_id])
    venue = relationship("Venue", back_populates="bookings")
    package = relationship("Package", back_populates="bookings")
    
    booking_vendors = relationship("BookingVendor", back_populates="booking", cascade="all, delete-orphan")
    booking_menus = relationship("BookingMenu", back_populates="booking", cascade="all, delete-orphan")
    guests = relationship("Guest", back_populates="booking", cascade="all, delete-orphan")
    invitation = relationship("Invitation", back_populates="booking", uselist=False, cascade="all, delete-orphan")
    tables = relationship("ReceptionTable", back_populates="booking", cascade="all, delete-orphan")
    budget = relationship("Budget", back_populates="booking", uselist=False, cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")
    schedules = relationship("EventSchedule", back_populates="booking", cascade="all, delete-orphan", order_by="EventSchedule.order_index")
    feedback = relationship("Feedback", back_populates="booking", uselist=False, cascade="all, delete-orphan")
