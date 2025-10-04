# AI-Powered Medical Student Trainer

An interactive backend system that simulates realistic patient conversations for medical training. This backend allows learners to ask questions, submit diagnoses, and receive contextual feedback powered by the Mistral language model.

## Features

* REST API built with FastAPI
* Conversational flow powered by Mistral API
* Supports realistic symptom-based case simulation
* Modular components for chatbot, memory, RAG, evaluation
* Suitable for integration with web or mobile frontend

## Project Structure

```
├── models/           # Interfaces to language and embedding models
├── prompts/          # Prompt templates for conversation and evaluation
├── rag/              # Retrieval-Augmented Generation logic
├── state/            # Session and dialogue state tracking
├── API_KEYS.py       # API key and environment configuration (Mistral)
├── chatbot.py        # Core chatbot logic
├── data_store.py     # In-memory or vector store for context
├── evaluation.py     # Diagnosis scoring and feedback logic
├── generator.py      # Synthetic patient case generator
├── main.py           # FastAPI entry point
├── sample.py         # Basic test or usage script
├── schemas.py        # Pydantic models for API input/output
└── README.md
```

## Requirements

* Python 3.8+
* Mistral API key
* Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

## Running the Server

1. Clone the repository:

   ```bash
   git clone https://github.com/Ponmurugaiya/AI-Medical-Student-Trainer.git
   cd AI-Medical-Student-Trainer
   ```

2. Set your Mistral API key in `API_KEYS.py`

3. Start the API server:

   ```bash
   uvicorn main:app --reload
   ```

4. Open your browser to:

   ```
   http://127.0.0.1:8000/docs
   ```

## Example Endpoints

* `POST /chat`: Send a user question or diagnosis
* `POST /evaluate`: Submit final diagnosis for evaluation
* `GET /state`: Get current session memory and interaction history

## Notes

* Mistral is used for both conversation generation and diagnosis evaluation
* Prompts are separated for easier customization
* Frontend integration is planned for future versions
