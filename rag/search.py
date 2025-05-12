# rag/search.py

import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS index and metadata store
INDEX_PATH = "backend2//rag//faiss_index.bin"
META_PATH = "backend2//rag//metadata.pkl"

def embed(texts):
    return model.encode(texts, convert_to_numpy=True)

def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def search_relevant_chunks(query, top_k=3):
    index, metadata = load_index()
    query_vector = embed([query])
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i] for i in indices[0]]
