import uuid
import json
import json5  # forgiving JSON parser
from models.mistral_api import call_mistral

def load_prompt_template():
    with open("P:\\Symptom_simulator\\AI-Symptom-Simulator\\backend2\\prompts\\case_prompt.txt", "r") as f:
        return f.read()

def generate_patient_case():
    prompt = load_prompt_template()

    messages = [
        {"role": "system", "content": "You are a helpful medical assistant who generates training cases for students. Respond ONLY in strict JSON."},
        {"role": "user", "content": prompt}
    ]

    response = call_mistral(messages)

    try:
        # Try parsing strict JSON
        case_data = json.loads(response)
    except json.JSONDecodeError:
        print("Standard JSON parsing failed. Trying json5...")
        try:
            case_data = json5.loads(response)
        except Exception as e:
            print("JSON5 parsing failed:", e)
            print("Raw response:\n", response)
            raise ValueError("Invalid JSON from LLM") from e

    case_data["id"] = str(uuid.uuid4())
    return case_data
