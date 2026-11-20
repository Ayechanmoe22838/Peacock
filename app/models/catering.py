from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # Appetizer, Main Course, Soup, Dessert, Beverage, Traditional Myanmar, Buffet Package
    description = Column(Text, nullable=True)
    price_per_person = Column(Numeric(12, 2), nullable=False)
    image_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking_associations = relationship("BookingMenu", back_populates="menu", cascade="all, delete-orphan")

class BookingMenu(Base):
    __tablename__ = "booking_menus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)  # Number of guest portions
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    dietary_notes = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="booking_menus")
    menu = relationship("Menu", back_populates="booking_associations")
