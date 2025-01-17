from fastapi import FastAPI, Depends, HTTPException, status,APIRouter,Response
from pydantic import BaseModel
from typing import Optional, Dict, List, Annotated
from datetime import date
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    condition: str
    patient_id: Optional[int] = None
    blood_group: Optional[str] = None
    mobile: Optional[str] = None
    visits: Optional[Dict[date, str]] = None
    payments: Optional[Dict[date, float]] = None
    prescriptions: Optional[Dict[date, List[str]]] = None
    insurance: Optional[Dict[str, str]] = None
    facilities_used: Optional[List[str]] = None

    class Config:
        orm_mode=True
        from_attribute=True

def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db_connection)]

@app.post("/patients/")
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


@app.get("/patients/{id}")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
