# MediSaarthi Backend API

Base URL:

http://localhost:8000

## Patients

### Create patient

POST /patients/

### Get patient

GET /patients/{patient_id}

### Get all patients

GET /patients/

## Interviews

### Start interview

POST /interview/start

### Save response

POST /interview/respond

### Complete interview

POST /interview/complete/{interview_id}

### Get interview

GET /interview/{interview_id}

## History

### Get patient history

GET /patients/{patient_id}/history