from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import supabase


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


class PatientCreate(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    language: str = "en"


@router.post("/")
def create_patient(patient: PatientCreate):

    # Check if patient already exists
    existing = (
        supabase
        .table("patients")
        .select("*")
        .eq("patient_id", patient.patient_id)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=409,
            detail="Patient already exists"
        )

    # Insert patient
    response = (
        supabase
        .table("patients")
        .insert(patient.model_dump())
        .execute()
    )

    return {
        "message": "Patient created successfully",
        "patient": response.data[0]
    }


@router.get("/{patient_id}")
def get_patient(patient_id: str):

    response = (
        supabase
        .table("patients")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return response.data[0]


@router.get("/")
def get_patients():

    response = (
        supabase
        .table("patients")
        .select("*")
        .execute()
    )

    return {
        "patients": response.data
    }