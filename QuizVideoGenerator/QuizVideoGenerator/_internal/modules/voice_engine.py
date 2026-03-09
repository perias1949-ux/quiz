import os
from google import genai
from google.genai import types
from app.config import settings
import uuid

def generate_voice_narration(text: str, output_filename: str | None = None) -> str:
    """
    Generate voice narration for the given text using Gemini TTS.
    If GEMINI_API_KEY is not set, we'll create a dummy empty wav file.
    Output is saved to the /audio folder.
    """
    if not output_filename:
        output_filename = f"{uuid.uuid4().hex}.wav"
        
    output_path = os.path.join("audio", output_filename)
        
    if not settings.GEMINI_API_KEY:
        with open(output_path, "wb") as f:
            f.write(b"") 
        return output_path
        
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Puck" # Enthusiastic voice suitable for quiz
                        )
                    )
                )
            )
        )
        
        # Extract audio bytes
        audio_bytes = response.candidates[0].content.parts[0].inline_data.data
        
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
                
        return output_path
    except Exception as e:
        print(f"Error generating voice via Gemini: {e}")
        with open(output_path, "wb") as f:
            f.write(b"")
        return output_path
