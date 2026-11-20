from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    budget_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), unique=True, nullable=False)
    total_budget = Column(Numeric(12, 2), default=0.00, nullable=False)
    estimated_cost = Column(Numeric(12, 2), default=0.00, nullable=False)
    actual_spent = Column(Numeric(12, 2), default=0.00, nullable=False)
    remaining_budget = Column(Numeric(12, 2), default=0.00, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="budget")
    expenses = relationship("Expense", back_populates="budget", cascade="all, delete-orphan")

class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    budget_id = Column(Integer, ForeignKey("budgets.budget_id", ondelete="CASCADE"), nullable=False)
    category = Column(String(50), nullable=False)  # Venue, Package, Catering, Vendors, Attire, Rings, Invitations, Transportation, Miscellaneous
    item_name = Column(String(150), nullable=False)
    estimated_cost = Column(Numeric(12, 2), default=0.00, nullable=False)
    actual_cost = Column(Numeric(12, 2), default=0.00, nullable=False)
    is_paid = Column(Boolean, default=False, nullable=False)
    payment_reference = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    budget = relationship("Budget", back_populates="expenses")
