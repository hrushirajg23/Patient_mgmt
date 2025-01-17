from sqlalchemy import Column, JSON, Integer, String, ForeignKey
from database import Base

class patient_registry(Base):
    __tablename__ = 'patient_registry'
    patient_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    gender = Column(String, index=True)  # Fixed case
    condition = Column(String, index=True)
    blood_group = Column(String, index=True)
    mobile = Column(String, index=True)
    visits = Column(JSON)  # Removed index
    payments = Column(JSON)
    prescriptions = Column(JSON)
    insurance = Column(JSON)
    facilities_used = Column(JSON)

class doctor_registry(Base):
    __tablename__ = 'doctor_registry'
    doctor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    gender = Column(String, index=True)  # Fixed case
    speciality = Column(String, index=True)
    payments = Column(JSON)
    patients_under = Column(JSON, ForeignKey("patient_registry.patient_id"))  # Fixed FK reference
