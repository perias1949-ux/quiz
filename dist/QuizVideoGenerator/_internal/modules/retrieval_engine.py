import math

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))
    
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0
        
    return dot_product / (magnitude_v1 * magnitude_v2)

def retrieve_relevant_chunks(query_embedding: list[float], chunks: list[dict], top_k: int = 5) -> list[dict]:
    """
    Retrieve top_k relevant chunks based on cosine similarity.
    chunks should be a list of mapping {"text": str, "embedding": list[float]}
    """
    similarities = []
    for chunk in chunks:
        # Some robustness checks
        if not chunk.get("embedding"):
            continue
        sim = cosine_similarity(query_embedding, chunk["embedding"])
        similarities.append((sim, chunk))
        
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in similarities[:top_k]]
