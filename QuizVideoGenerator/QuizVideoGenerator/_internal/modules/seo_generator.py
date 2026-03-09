import json
import os
from google import genai
from google.genai import types
from app.config import settings
import uuid
from pydantic import BaseModel
from typing import List

class YouTubeSEOSchema(BaseModel):
    title: str
    description: str
    tags: List[str]

def generate_seo_metadata(topic: str, questions: list[dict], output_filename: str | None = None) -> dict:
    """Generate YouTube SEO metadata via Gemini SDK."""
    if not output_filename:
        output_filename = f"video_metadata_{str(uuid.uuid4())[:8]}.json"
        
    output_path = os.path.join("metadata", output_filename)
        
    if not settings.GEMINI_API_KEY:
        data = {
            "title": f"Ultimate {topic} Quiz | Can You Score 20/20?",
            "description": f"Test your knowledge on {topic} with this quiz!\n\nThis quiz is intended for educational and entertainment purposes only and should not be considered medical or psychological advice.",
            "tags": [f"{topic.lower()} quiz", "knowledge quiz", "trivia"]
        }
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        return data

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = f"""
    You are an expert YouTube SEO manager. Generate the following metadata for a quiz video about "{topic}":
    1. A catchy 'title' (under 60 characters)
    2. A 'description' (including a default 2 sentence disclaimer about not being medical/psychological advice but educational)
    3. A list of 10 relevant 'tags'
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=YouTubeSEOSchema,
                temperature=0.7
            )
        )
        
        data = json.loads(response.text)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        return data
    except Exception as e:
        print(f"Error generating SEO via Gemini: {e}")
        return {}
