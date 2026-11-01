import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load variables from .env file if present
load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "Multilingual Government Service Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # CORS Origins allowed to communicate with this backend
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://voicebot-thnn.onrender.com",
        "https://sevamitra-the-voicebot.onrender.com",
    ] + [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "").split(",") if x.strip()]
    
    # Speech & Language APIs (Configurable via .env)
    BHASHINI_USER_ID: str = os.getenv("BHASHINI_USER_ID", "")
    BHASHINI_API_KEY: str = os.getenv("BHASHINI_API_KEY", "")
    BHASHINI_PIPELINE_ID: str = os.getenv("BHASHINI_PIPELINE_ID", "")
    
    # LLM Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
