from uuid import UUID
from pydantic import BaseModel
from datetime import datetime, date
from typing import Any, Optional, Literal, List, Dict
import re


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
        from_attribute=True

