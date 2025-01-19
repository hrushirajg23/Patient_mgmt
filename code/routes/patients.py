from fastapi import APIRouter, Depends, HTTPException, status, Body, UploadFile, File
from sqlalchemy.orm import Session
from re import compile
from uuid import uuid4
import zoneinfo
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from database import get_db
from models import *
from config import setting

route = APIRouter(prefix="/profile", tags=["Profile"])
@route.post("/patients/")
async def create_patient(name: str,
        age: int,
        gender: str,
        condition: str,
        blood_group: str,
        mobile: str,
        db: db_dependency):
    db_patient = models.patient_registry(
        name=name,
        age=age,
        gender=gender,
        condition=condition,
        blood_group=blood_group,
        mobile=mobile,
        visits=None,
        payments=None,
        prescriptions=None,
        insurance=None,
        facilities_used=None,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return {"message": "Patient created successfully", "patient_id": db_patient.patient_id}


@route.get("/patients/{id}")
async def get_patient(id: int, db: db_dependency):
    query = db.query(models.patient_registry).filter(models.patient_registry.patient_id == id)
    db_patient = query.first()

    if not db_patient:
        raise HTTPException(
            status_code=404,
            detail=f"No patient with id: {id}"
        )

    # Serialize using model_validate with from_attributes enabled
    patient_data = Patient.model_validate(db_patient)
    return {"status": "success", "patient": patient_data}

    