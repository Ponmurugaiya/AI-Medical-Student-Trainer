# evaluation.py

from schemas import DiagnosisSubmission, DiagnosisEvaluationResponse, AccuracyStats
from data_store import patient_cases, accuracy_stats

def submit_diagnosis_logic(payload: DiagnosisSubmission) -> DiagnosisEvaluationResponse:
    case = patient_cases.get(payload.case_id)
    if not case:
        raise ValueError("Case not found")

    true_diagnosis = case.get("diagnosis", "").lower().strip()
    student_guess = payload.diagnosis_guess.lower().strip()

    is_correct = (true_diagnosis == student_guess)

    # Update global stats
    accuracy_stats["total"] += 1
    if is_correct:
        accuracy_stats["correct"] += 1

    # Per-disease stats
    disease = case["diagnosis"]
    if disease not in accuracy_stats["per_disease"]:
        accuracy_stats["per_disease"][disease] = {"total": 0, "correct": 0}

    accuracy_stats["per_disease"][disease]["total"] += 1
    if is_correct:
        accuracy_stats["per_disease"][disease]["correct"] += 1

    return DiagnosisEvaluationResponse(
        correct=is_correct,
        actual_diagnosis=case["diagnosis"],
        case_difficulty=case["difficulty"]
    )

def get_accuracy_stats_logic() -> AccuracyStats:
    total = accuracy_stats["total"]
    correct = accuracy_stats["correct"]

    per_disease_accuracy = {
        disease: round((stats["correct"] / stats["total"]) * 100, 2)
        for disease, stats in accuracy_stats["per_disease"].items()
    }

    return AccuracyStats(
        total_attempts=total,
        correct_attempts=correct,
        accuracy_percentage=round((correct / total) * 100, 2) if total > 0 else 0.0,
        per_disease_accuracy=per_disease_accuracy
    )
