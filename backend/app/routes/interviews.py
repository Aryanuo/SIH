from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import supabase
import uuid

router = APIRouter(
    prefix="/interview",
    tags=["Interviews"]
)


class InterviewStart(BaseModel):
    patient_id: str


class InterviewResponse(BaseModel):
    interview_id: str
    question: str
    answer: str
    question_number: int


@router.post("/start")
def start_interview(data: InterviewStart):

    # Check that patient exists
    patient = (
        supabase
        .table("patients")
        .select("patient_id")
        .eq("patient_id", data.patient_id)
        .execute()
    )

    if not patient.data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Generate interview ID
    existing = (
        supabase
        .table("interviews")
        .select("interview_id")
        .order("started_at", desc=True)
        .limit(1)
        .execute()
    )

    if existing.data:
        last_id = existing.data[0]["interview_id"]
        number = int(last_id.replace("INT", "")) + 1
    else:
        number = 1

    interview_id = f"INT-{uuid.uuid4().hex[:8].upper()}"

    # Create interview
    response = (
        supabase
        .table("interviews")
        .insert({
            "interview_id": interview_id,
            "patient_id": data.patient_id,
            "status": "active"
        })
        .execute()
    )

    return {
        "message": "Interview started successfully",
        "interview": response.data[0]
    }


@router.post("/respond")
def save_response(data: InterviewResponse):

    # Check interview exists
    interview = (
        supabase
        .table("interviews")
        .select("interview_id, status")
        .eq("interview_id", data.interview_id)
        .execute()
    )

    if not interview.data:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    if interview.data[0]["status"] == "completed":
        raise HTTPException(
            status_code=400,
            detail="Interview is already completed"
        )

    # Store response
    response = (
        supabase
        .table("interview_responses")
        .insert({
            "interview_id": data.interview_id,
            "question": data.question,
            "answer": data.answer,
            "question_number": data.question_number
        })
        .execute()
    )

    return {
        "message": "Response saved successfully",
        "response": response.data[0]
    }


@router.post("/complete/{interview_id}")
def complete_interview(interview_id: str):

    # Check interview exists
    existing = (
        supabase
        .table("interviews")
        .select("*")
        .eq("interview_id", interview_id)
        .execute()
    )

    if not existing.data:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    if existing.data[0]["status"] == "completed":
        raise HTTPException(
            status_code=400,
            detail="Interview is already completed"
        )

    # Mark completed
    response = (
        supabase
        .table("interviews")
        .update({
            "status": "completed"
        })
        .eq("interview_id", interview_id)
        .execute()
    )

    return {
        "message": "Interview completed successfully",
        "interview": response.data[0]
    }


@router.get("/{interview_id}")
def get_interview(interview_id: str):

    interview = (
        supabase
        .table("interviews")
        .select("*")
        .eq("interview_id", interview_id)
        .execute()
    )

    if not interview.data:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    responses = (
        supabase
        .table("interview_responses")
        .select("*")
        .eq("interview_id", interview_id)
        .order("question_number")
        .execute()
    )

    return {
        "interview": interview.data[0],
        "responses": responses.data
    }