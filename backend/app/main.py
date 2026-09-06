from fastapi import FastAPI

from app.routes.patients import router as patient_router
from app.routes.interviews import router as interview_router
from app.routes.history import router as history_router


app = FastAPI(
    title="MediSaarthi Backend",
    description="Backend API for the AI-powered Pre-Consultation Intelligence Platform",
    version="1.0.0"
)


app.include_router(patient_router)
app.include_router(interview_router)
app.include_router(history_router)


@app.get("/")
def root():
    return {
        "message": "MediSaarthi Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }