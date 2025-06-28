import numpy as np
from .vectorizer import vectorize_query, unpickle_vector
from sqlalchemy.orm import Session
from app.db import models

def semantic_search(query: str, db_entries, limit: int = 10):
    """
    Perform semantic search with pagination.
    
    Args:
        query: Search query string
        db_entries: Database entries to search through
        limit: Maximum number of results to return
    
    Returns:
        List of (score, entry) tuples sorted by score
    """
    query_vec = unpickle_vector(vectorize_query(query))
    similarities = []
    
    for entry in db_entries:
        entry_vec = unpickle_vector(entry.vector)
        sim = np.dot(query_vec, entry_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(entry_vec))
        similarities.append((sim, entry))
    
    # Sort by similarity score (highest first) and limit results
    similarities.sort(reverse=True, key=lambda x: x[0])
    return similarities[:limit]

def search_by_id(query: str, db_entries, limit: int = 10):
    """
    Search specifically by ID for better accuracy.
    """
    query_vec = unpickle_vector(vectorize_query(query))
    similarities = []
    
    for entry in db_entries:
        if hasattr(entry, 'id_vector') and entry.id_vector:
            entry_vec = unpickle_vector(entry.id_vector)
            sim = np.dot(query_vec, entry_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(entry_vec))
            similarities.append((sim, entry))
    
    similarities.sort(reverse=True, key=lambda x: x[0])
    print(similarities)
    return similarities[:limit]

def search_by_name(query: str, db_entries, limit: int = 10):
    """
    Search specifically by name for better accuracy.
    """
    query_vec = unpickle_vector(vectorize_query(query))
    similarities = []
    
    for entry in db_entries:
        if hasattr(entry, 'name_vector') and entry.name_vector:
            entry_vec = unpickle_vector(entry.name_vector)
            sim = np.dot(query_vec, entry_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(entry_vec))
            similarities.append((sim, entry))
    
    similarities.sort(reverse=True, key=lambda x: x[0])
    return similarities[:limit]

def smart_search(query: str, db_entries, limit: int = 10):
    """
    Smart search that tries ID first, then name, then combined.
    """
    # Check if query looks like an ID (numeric)
    if query.isdigit():
        # Try ID search first
        id_results = search_by_id(query, db_entries, limit)
        if id_results:
            return id_results
    
    # Try name search
    name_results = search_by_name(query, db_entries, limit)
    if name_results:
        return name_results
    
    # Fall back to combined search
    return semantic_search(query, db_entries, limit)

def get_best_match(query: str, db_entries):
    """
    Get only the best (first) semantic match using smart search.
    
    Args:
        query: Search query string
        db_entries: Database entries to search through
    
    Returns:
        Tuple of (score, entry) for the best match, or None if no match
    """
    results = smart_search(query, db_entries, limit=1)
    return results[0] if results else None


def batch_vectorize_texts(texts: list) -> list:
    """
    Vectorize multiple texts in batch for better performance.
    """
    from .vectorizer import model
    vectors = model.encode(texts)
    return vectors 