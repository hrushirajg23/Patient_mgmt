'''
@Author: Hrushiraj Gandhi
@Date: 14 jan 2025
@goal:
     a) To build patient management system 
     b) Use fastapi , postgresql
     c) Perform more operations than CRUD
     
'''
from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

class Patient(BaseModel):
    name: str
    age: int
    condition: str
    patient_id: Optional[int] = None
    blood_group: Optional[str] = None
    mobile: Optional[str] = None

patients_registry: Dict[int, Patient] = {}

def get_db_connection():
    return psycopg2.connect(
        dbname="patient_db", 
        user="hrushiraj", 
        password="root", 
        host="localhost", 
        port="5432"
    )

@app.put("/register")
def create_patient(name: str, age: int, condition: str, blood_group: Optional[str] = None, mobile: Optional[str] = None) -> Patient:
    patient_id = len(patients_registry) + 1
    patient = Patient(name=name, age=age, condition=condition, blood_group=blood_group, mobile=mobile, patient_id=patient_id)
    patients_registry[patient_id] = patient
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patient_registry (patient_id, name, age, condition, blood_group, mobile) VALUES (%s, %s, %s, %s, %s, %s)",
            (patient_id, name, age, condition, blood_group, mobile)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return patient

@app.get("/show_patient_status")
def show_patient_status(name: str, patient_id: int = None) -> Patient:
    if patient_id is not None:
        patient = patients_registry.get(patient_id)
        if patient and patient.name == name:
            return patient
        raise HTTPException(status_code=404, detail="Patient ID not found")
    else:
        for patient_id, patient in patients_registry.items():
            if patient.name == name:
                return patient
        raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/update_my_details")
def update_my_details(patient_id: int, name: Optional[str] = None, age: Optional[int] = None, condition: Optional[str] = None, blood_group: Optional[str] = None, mobile: Optional[str] = None):
    if patient_id not in patients_registry:
        raise HTTPException(status_code=404, detail="Patient ID not found")
    
    patient = patients_registry[patient_id]
    if name:
        patient.name = name
    if age:
        patient.age = age
    if condition:
        patient.condition = condition
    if blood_group:
        patient.blood_group = blood_group
    if mobile:
        patient.mobile = mobile
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE patient_registry SET name = %s, age = %s, condition = %s, blood_group = %s, mobile = %s WHERE patient_id = %s",
            (patient.name, patient.age, patient.condition, patient.blood_group, patient.mobile, patient_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Patient details updated successfully"}

'''
     Other methods

     1. 
'''