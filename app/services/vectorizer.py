from sentence_transformers import SentenceTransformer
import numpy as np
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

def vectorize_id_name(id_value: str, name: str) -> bytes:
    combined = f"{id_value} {name}"
    vec = model.encode([combined])[0]
    return pickle.dumps(vec)

def vectorize_id_only(id_value: str) -> bytes:
    # Vectorize ID separately for exact ID matching
    vec = model.encode([id_value])[0]
    return pickle.dumps(vec)

def vectorize_name_only(name: str) -> bytes:
    # Vectorize name separately for name-only matching
    vec = model.encode([name])[0]
    return pickle.dumps(vec)

def vectorize_query(query: str) -> bytes:
    # For search, treat the query as a combined id/name string
    vec = model.encode([query])[0]
    return pickle.dumps(vec)

def unpickle_vector(blob: bytes) -> np.ndarray:
    return pickle.loads(blob) 