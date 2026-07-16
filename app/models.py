from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String)
    availability = Column(String)

    appointments = relationship("Appointment", back_populates="doctor")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String)
    owner = Column(String)

    appointments = relationship("Appointment", back_populates="pet")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    pet_id = Column(Integer, ForeignKey("pets.id"))

    date = Column(String)
    time = Column(String)

    doctor = relationship("Doctor", back_populates="appointments")
    pet = relationship("Pet", back_populates="appointments")