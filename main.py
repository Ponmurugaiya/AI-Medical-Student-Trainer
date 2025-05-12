from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from generator import generate_patient_case
from chatbot import ask_patient, submit_diagnosis_logic

from rag.build_index import build_faiss_index
from schemas import (
    DiagnosisSubmission, DiagnosisEvaluationResponse,
    AccuracyStats, StudentQuestion, PatientResponse
)
from data_store import patient_cases, accuracy_stats
from state import session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-powered Symptom Simulator API. Go to /docs for Swagger UI."}

@app.post("/generate_case")
def generate_case():
    case = generate_patient_case()
    patient_cases["current"] = case
    build_faiss_index([case])
    return case

@app.post("/ask_patient", response_model=PatientResponse)
def ask_patient_endpoint(payload: StudentQuestion):
    patient_answer = ask_patient(payload.question)

    # Append to in-memory conversation
    session.session_state["conversation"].append(patient_answer)

    return patient_answer




@app.post("/submit_diagnosis", response_model=DiagnosisEvaluationResponse)
def submit_diagnosis(payload: DiagnosisSubmission):
    conversation = session.session_state["conversation"]
    correct_diagnosis = patient_cases.get("current", {}).get("diagnosis", "").lower().strip()
        
    return submit_diagnosis_logic(payload.diagnosis_guess, conversation, correct_diagnosis)


