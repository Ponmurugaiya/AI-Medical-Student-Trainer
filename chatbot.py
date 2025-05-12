# chatbot.py

from rag.search import search_relevant_chunks
from models.mistral_api import call_mistral
from schemas import DiagnosisSubmission, DiagnosisEvaluationResponse, AccuracyStats
import json
import re

def ask_patient(student_question: str):
    # Search for relevant info using RAG
    context_chunks = search_relevant_chunks(student_question)

    context = "\n".join(context_chunks)

    messages = [
        {"role": "system", "content": "You are a patient simulator answering a medical student's question."},
        {"role": "user", "content": f"""The following context is extracted from your medical case:

{context}

Question: {student_question}
Only respond asked question by single word or sentence like a patient, You must don't reveal any extra info unless asked just answer to the question with word.
if the information not provided and you can answer but please don't mention like "this is an assumption" or anything just give the answer only
"""}
    ]

    response = call_mistral(messages)
    cleaned_response = re.sub(r'\([^)]*\)', '', response)
    return {
        "question": student_question,
        "answer": cleaned_response
    }

def submit_diagnosis_logic(diagnosis_guess: str, conversation: list[dict], ground_truth: str) -> DiagnosisEvaluationResponse:

    # Format the actual conversation
    formatted_conversation = "\n".join([
        f"Student: {turn['question']}\nPatient: {turn['answer']}" for turn in conversation
    ])

    # Construct prompt to avoid hallucinated conversation
    messages = [
        {
            "role": "system",
            "content": "You are a medical assistant evaluating a medical student's diagnosis skills based on their conversation with a simulated patient."
        },
        {
            "role": "user",
            "content": f"""
Here is the actual conversation between student and patient:

{formatted_conversation}

The student's guess: {diagnosis_guess}
Correct diagnosis: {ground_truth}

Your task:
- Tell whether the guess is correct.
- Identify important clues from the conversation that support or contradict the guess.
- Suggest questions or areas the student could have explored better.

Please respond in this exact JSON format:

{{
  "correct": true or false by analyzing the student's guess and correct diagnosis,
  "clues": [list of clues from the conversation and if the student guess is correct then appreciate with that],
  "suggestions": [list of suggestions for improvement and if the student guess is correct then appreciate with that]
}}
"""
        }
    ]

    # Call LLM
    llm_response_raw = call_mistral(messages)

    # Try to parse as JSON
    try:
        llm_data = json.loads(llm_response_raw)
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON from LLM: {llm_response_raw}")

    # Construct final response using actual conversation and ground truth
    clues = llm_data.get("clues", [])
    suggestions = llm_data.get("suggestions", [])

    all_suggestions = [
        item["text"]
        for item in clues + suggestions
        if isinstance(item, dict) and "text" in item
    ]

    return DiagnosisEvaluationResponse(
    correct=llm_data["correct"],
    correct_diagnosis=ground_truth,
    conversation=conversation,
    suggestions=all_suggestions
)

