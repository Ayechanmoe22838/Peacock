from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class ReceptionTable(Base):
    __tablename__ = "reception_tables"

    table_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    table_number = Column(Integer, nullable=False)
    table_name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False, default=10)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="tables")
    assignments = relationship("SeatingAssignment", back_populates="table", cascade="all, delete-orphan")

class SeatingAssignment(Base):
    __tablename__ = "seating_assignments"

    assignment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    table_id = Column(Integer, ForeignKey("reception_tables.table_id", ondelete="CASCADE"), nullable=False)
    guest_id = Column(Integer, ForeignKey("guests.guest_id", ondelete="CASCADE"), unique=True, nullable=False)
    seat_number = Column(Integer, nullable=True)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    table = relationship("ReceptionTable", back_populates="assignments")
    guest = relationship("Guest", back_populates="seating_assignment")
