from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Package(Base):
    __tablename__ = "packages"

    package_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    package_name = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    status = Column(String(20), default="active", nullable=False)  # 'active', 'inactive'
    is_active = Column(Boolean, default=True, nullable=False)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    services = relationship("PackageService", back_populates="package", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="package")

class PackageService(Base):
    __tablename__ = "package_services"

    service_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey("packages.package_id", ondelete="CASCADE"), nullable=False)
    service_name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    is_included = Column(Boolean, default=True, nullable=False)

    package = relationship("Package", back_populates="services")
