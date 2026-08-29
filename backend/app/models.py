from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class DbUser(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    role = Column(String, default="parent")  # parent | health_worker | admin
    phone = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    preferred_lang = Column(String, default="en")
    area = Column(String, nullable=False)

class DbFamily(Base):
    __tablename__ = "families"

    id = Column(String, primary_key=True, index=True)
    primary_phone = Column(String, unique=True, nullable=False)
    consent_given_at = Column(DateTime, default=datetime.utcnow)
    consent_version = Column(String, default="1.0")

    children = relationship("DbChild", back_populates="family")

class DbChild(Base):
    __tablename__ = "children"

    id = Column(String, primary_key=True, index=True)
    family_id = Column(String, ForeignKey("families.id"), nullable=False)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    family = relationship("DbFamily", back_populates="children")
    doses = relationship("DbDoseRecord", back_populates="child", cascade="all, delete-orphan")

class DbDoseRecord(Base):
    __tablename__ = "dose_records"

    id = Column(String, primary_key=True, index=True)
    child_id = Column(String, ForeignKey("children.id"), nullable=False)
    vaccine_code = Column(String, nullable=False)
    status = Column(String, nullable=False)  # due | done | missed
    administered_date = Column(Date, nullable=True)
    administered_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("DbChild", back_populates="doses")

class DbCamp(Base):
    __tablename__ = "camps"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    area = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    created_by = Column(String, default="health_dept")
    total_capacity = Column(Integer, default=40)
    total_booked = Column(Integer, default=0)

    slots = relationship("DbCampSlot", back_populates="camp", cascade="all, delete-orphan")

class DbCampSlot(Base):
    __tablename__ = "camp_slots"

    id = Column(String, primary_key=True, index=True)
    camp_id = Column(String, ForeignKey("camps.id"), nullable=False)
    time_range = Column(String, nullable=False)  # e.g., "09:00 - 10:30 AM"
    capacity = Column(Integer, nullable=False)
    booked_count = Column(Integer, default=0)

    camp = relationship("DbCamp", back_populates="slots")

class DbBooking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, index=True)
    reference_code = Column(String, unique=True, index=True, nullable=False)
    camp_slot_id = Column(String, ForeignKey("camp_slots.id"), nullable=False)
    child_id = Column(String, ForeignKey("children.id"), nullable=False)
    family_id = Column(String, ForeignKey("families.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="CONFIRMED")
