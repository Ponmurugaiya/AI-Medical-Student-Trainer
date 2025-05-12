# In-memory store for patient cases
# Format: { case_id (str): case_dict (dict) }
patient_cases = {}

# In-memory accuracy tracker
accuracy_stats = {
    "total": 0,
    "correct": 0,
    "per_disease": {}  # { disease_name: { "total": int, "correct": int } }
}

