from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types
from app.config import settings
import json

class QuestionSchema(BaseModel):
    question: str
    A: str
    B: str
    C: str
    D: str
    answer: str # Must be exactly 'A', 'B', 'C', or 'D'

def get_genai_client():
    if not settings.GEMINI_API_KEY:
        return None
    return genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_questions_from_context(topic: str, context_chunks: list[str], count: int = 20) -> list[dict]:
    """Generate questions grounded strictly in the provided context chunks using Gemini Structured Outputs."""
    client = get_genai_client()
    
    if not client:
        return [
            {
                "question": f"Dummy Question {i+1} for {topic}?",
                "A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D",
                "answer": "A"
            } for i in range(count)
        ]
        
    context_text = "\n\n---\n\n".join(context_chunks)
    
    prompt = f"""
    You are an expert quiz creator. Generate exactly {count} multiple choice questions about "{topic}".
    RULES:
    1. Ground all questions STRICTLY in the provided text. Do not hallucinate outside information.
    2. Provide 4 options (A, B, C, D) and specify the correct answer letter.
    3. Return exactly {count} questions.
    
    CONTEXT TEXT:
    {context_text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=List[QuestionSchema],
                temperature=0.3
            )
        )
        # GenAI SDK returns JSON string when schema is provided
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating Gemini questions: {e}")
        return []
