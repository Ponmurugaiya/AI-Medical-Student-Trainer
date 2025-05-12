# schemas.py

from pydantic import BaseModel
from typing import List, Dict, Optional

class PainDetails(BaseModel):
    location: str
    severity: str
    type: str
    timing: str

class VitalSigns(BaseModel):
    temperature: str
    bp: str
    pulse: str
    respiratory_rate: str
    oxygen_saturation: str

class SystemWiseFindings(BaseModel):
    respiratory: str
    cardiovascular: str
    abdominal: str
    neurological: str
    dermatological: str

class PatientCase(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    ethnicity: str
    marital_status: str
    education_level: str
    language_spoken: str
    occupation: str
    living_conditions: str
    travel_history: str
    animal_exposure: str
    substance_use: str
    sexual_history: str
    support_system: str
    past_illnesses: List[str]
    surgical_history: List[str]
    medication_history: List[str]
    allergies: List[str]
    vaccination_history: List[str]
    hospitalization_history: List[str]
    menstrual_history: str
    obstetric_history: str
    contraception: str
    presenting_complaints: List[str]
    symptom_onset_duration: str
    symptom_progression: str
    associated_symptoms: List[str]
    aggravating_factors: List[str]
    relieving_factors: List[str]
    pain_details: PainDetails
    general_appearance: str
    vital_signs: VitalSigns
    system_wise_findings: SystemWiseFindings
    lab_results: Dict[str, str]
    imaging_results: Dict[str, str]
    special_tests: Dict[str, str]
    diagnosis: str
    severity: str
    case_difficulty: str
    notes_for_ai: str
    red_herrings: List[str]
    teaching_points: List[str]
    differential_diagnoses: List[str]
    communication_style: str

class DiagnosisSubmission(BaseModel):
    diagnosis_guess: str

class DiagnosisEvaluationResponse(BaseModel):
    correct: bool
    correct_diagnosis: str
    conversation: List[dict]
    suggestions: List[str]

class AccuracyStats(BaseModel):
    total_attempts: int
    correct_attempts: int
    accuracy_percentage: float
    per_disease_accuracy: Dict[str, float]


class StudentQuestion(BaseModel):
    question: str
    
class PatientResponse(BaseModel):
    answer: str