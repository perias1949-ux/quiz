from google import genai
from app.config import settings

def get_genai_client():
    if not settings.GEMINI_API_KEY:
        return None
    return genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for given texts using models/text-embedding-004."""
    client = get_genai_client()
    
    if not client:
        # Avoid crashing if we are just testing without keys, return dummy embeddings representing dim 768
        return [[0.0] * 768 for _ in texts]
        
    response = client.models.embed_content(
        model='text-embedding-004',
        contents=texts,
    )
    
    return [e.values for e in response.embeddings]
