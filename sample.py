from data_store import patient_cases

correct_diagnosis = patient_cases.get("0", {}).get("diagnosis", "").lower().strip()

print(correct_diagnosis)