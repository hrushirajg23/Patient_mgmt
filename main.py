from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import date

app = FastAPI()

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

def get_db_connection():
    return psycopg2.connect(
        dbname="patient_db", 
        user="hrushiraj", 
        password="root", 
        host="localhost", 
        port="5432"
    )

@app.post("/patients")
def create_patient(name: str, age: int, gender: str, condition: str, blood_group: Optional[str] = None, mobile: Optional[str] = None) -> Patient:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO patient_registry (name, age, gender, condition, blood_group, mobile)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING patient_id;
            """,
            (name, age, gender, condition, blood_group, mobile)
        )
        patient_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return Patient(name=name, age=age, gender=gender, condition=condition, blood_group=blood_group, mobile=mobile, patient_id=patient_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int) -> Patient:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient_registry WHERE patient_id = %s", (patient_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Patient(
                patient_id=row[0],
                name=row[1],
                age=row[2],
                gender=row[3],
                condition=row[4],
                blood_group=row[5],
                mobile=row[6]
            )
        else:
            raise HTTPException(status_code=404, detail="Patient not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, name: Optional[str] = None, age: Optional[int] = None, gender: Optional[str] = None, condition: Optional[str] = None, blood_group: Optional[str] = None, mobile: Optional[str] = None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        updates = []
        params = []
        if name:
            updates.append("name = %s")
            params.append(name)
        if age:
            updates.append("age = %s")
            params.append(age)
        if gender:
            updates.append("gender = %s")
            params.append(gender)
        if condition:
            updates.append("condition = %s")
            params.append(condition)
        if blood_group:
            updates.append("blood_group = %s")
            params.append(blood_group)
        if mobile:
            updates.append("mobile = %s")
            params.append(mobile)

        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(patient_id)
        cursor.execute(f"UPDATE patient_registry SET {', '.join(updates)} WHERE patient_id = %s", params)
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Patient updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patient_registry WHERE patient_id = %d", (patient_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Patient deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/patients/{patient_id}/medical_history")
def medical_history(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT visit_date, description FROM medical_history WHERE patient_id = %s", (patient_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            raise HTTPException(status_code=404, detail="No medical history found for this patient")

        history = {row[0]: row[1] for row in rows}
        return {"patient_id": patient_id, "medical_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/patients/{patient_id}/insurance")
def add_insurance(patient_id: int, insurance_provider: str, policy_number: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO insurance_info (patient_id, provider, policy_number) VALUES (%d, %s, %s)",
            (patient_id, insurance_provider, policy_number)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Insurance information added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/patients/{patient_id}/insurance")
def get_insurance(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT provider, policy_number FROM insurance_info WHERE patient_id = %s", (patient_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            raise HTTPException(status_code=404, detail="No insurance information found")

        insurance = {"provider": rows[0][0], "policy_number": rows[0][1]}
        return {"patient_id": patient_id, "insurance": insurance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/patients/{patient_id}/prescriptions")
def add_prescription(patient_id: int, date_prescribed: date, medicines: List[str]):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prescriptions (patient_id, date_prescribed, medicines) VALUES (%d, %s, %s)",
            (patient_id, date_prescribed, medicines)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Prescription added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/patients/{patient_id}/prescriptions")
def get_prescriptions(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date_prescribed, medicines FROM prescriptions WHERE patient_id = %d", (patient_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            raise HTTPException(status_code=404, detail="No prescriptions found")

        prescriptions = {row[0]: row[1] for row in rows}
        return {"patient_id": patient_id, "prescriptions": prescriptions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/patients/{patient_id}/facilities")
def add_facility_usage(patient_id: int, facility_name: str, usage_date: date):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO facility_usage (patient_id, facility_name, usage_date) VALUES (%s, %s, %s)",
            (patient_id, facility_name, usage_date)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Facility usage recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/patients/{patient_id}/facilities")
def get_facility_usage(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT facility_name, usage_date FROM facility_usage WHERE patient_id = %s", (patient_id,))
        rows = cursor.fetchall()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
