from fastapi import APIRouter, HTTPException
from app.database import supabase
from app.schemas import PatientHistoryResponse

router = APIRouter(
    prefix="/patients",
    tags=["Patient History"]
)


@router.get("/{patient_id}/history", response_model=PatientHistoryResponse)
def get_patient_history(patient_id: str):

    # Check patient exists
    patient = (
        supabase
        .table("patients")
        .select("patient_id, name, age, gender, language")
        .eq("patient_id", patient_id)
        .execute()
    )

    if not patient.data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Get medical history
    medical_history = (
        supabase
        .table("medical_history")
        .select("condition, diagnosed_year, notes")
        .eq("patient_id", patient_id)
        .order("diagnosed_year")
        .execute()
    )

    # Get medications
    medications = (
        supabase
        .table("medications")
        .select("name, dosage, frequency, notes")
        .eq("patient_id", patient_id)
        .execute()
    )

    # Get allergies
    allergies = (
        supabase
        .table("allergies")
        .select("allergen, reaction")
        .eq("patient_id", patient_id)
        .execute()
    )

    return {
        "patient": patient.data[0],
        "medical_history": medical_history.data,
        "medications": medications.data,
        "allergies": allergies.data
    }