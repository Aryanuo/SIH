from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import supabase
from app.schemas import PatientCreate, PatientResponse

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate):

    existing = (
        supabase
        .table("patients")
        .select("patient_id")
        .eq("patient_id", patient.patient_id)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=409,
            detail="Patient already exists"
        )

    response = (
        supabase
        .table("patients")
        .insert(patient.model_dump())
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create patient"
        )

    return response.data[0]


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str):

    response = (
        supabase
        .table("patients")
        .select(
            "patient_id, name, age, gender, language"
        )
        .eq("patient_id", patient_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return response.data[0]

@router.get("/", response_model=list[PatientResponse])
def get_patients():

    response = (
        supabase
        .table("patients")
        .select(
            "patient_id, name, age, gender, language"
        )
        .execute()
    )

    return response.data