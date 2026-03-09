from google import genai
from google.genai import types
from app.config import settings
import json

def get_genai_client():
    if not settings.GEMINI_API_KEY:
        return None
    return genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_quiz_topics(article_content: str, count: int = 5) -> list[str]:
    """Generate potential quiz topics from an article using Gemini."""
    client = get_genai_client()
    
    if not client:
        return ["General Knowledge Quiz", "Facts Quiz", "Summary Quiz"]
        
    prompt = f"Analyze the context and suggest {count} engaging quiz topics based on it. Context: {article_content[:5000]}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=list[str],
                temperature=0.7
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing Gemini topics: {e}")
        return ["General Quiz"]
