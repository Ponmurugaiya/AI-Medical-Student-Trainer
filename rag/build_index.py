# rag/build_index.py

import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_case(case: dict):
    chunks = []
    for key, value in case.items():
        if isinstance(value, (str, list, dict)):
            chunks.append(f"{key}: {value}")
    return chunks

def build_faiss_index(cases):
    texts = []
    metadata = []

    for case in cases:
        chunks = chunk_case(case)
        texts.extend(chunks)
        metadata.extend(chunks)

    embeddings = model.encode(texts, convert_to_numpy=True)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # ✅ Ensure rag/ directory exists
    os.makedirs("backend2/rag", exist_ok=True)

    faiss.write_index(index, "backend2//rag//faiss_index.bin")
    print("✅faiss_index.bin Successfully created")
    with open("backend2//rag//metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)
    print("✅metadata.pkl Successfully created")
