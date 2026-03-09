from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Quiz Video Generator"
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./quiz.db" # Default fallback

    class Config:
        env_file = ".env"

settings = Settings()
