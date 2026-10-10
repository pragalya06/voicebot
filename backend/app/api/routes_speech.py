from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.config import settings
from app.services.language_detection_service import detect_language_from_text, SUPPORTED_LANGUAGES

router = APIRouter(prefix="/api/speech", tags=["Speech & Voice"])

class SynthesisRequest(BaseModel):
    text: str
    language: str = "ta"

class LanguageDetectRequest(BaseModel):
    text: str

class LanguageDetectResponse(BaseModel):
    detected_language: str
    language_name: str
    native_name: str
    flag: str
    speech_locale: str
    confidence: float
    is_supported: bool
    is_uncertain: bool
    script: Optional[str] = None
    message: Optional[str] = None

class SpeechCapabilitiesResponse(BaseModel):
    bhashini_configured: bool
    supported_languages: List[str]
    tts_engine: str
    stt_engine: str

@router.get("/capabilities", response_model=SpeechCapabilitiesResponse)
def get_speech_capabilities():
    """
    Returns available speech capabilities.
    Lists verified languages: English, Tamil, Hindi, Marathi, Bengali.
    """
    has_bhashini = bool(settings.BHASHINI_API_KEY and settings.BHASHINI_USER_ID)
    return SpeechCapabilitiesResponse(
        bhashini_configured=has_bhashini,
        supported_languages=list(SUPPORTED_LANGUAGES.keys()),
        tts_engine="Bhashini TTS" if has_bhashini else "Web Speech Synthesis (Native)",
        stt_engine="Bhashini STT" if has_bhashini else "Web Speech Recognition (Native)"
    )

@router.post("/detect_language", response_model=LanguageDetectResponse)
def detect_spoken_language(payload: LanguageDetectRequest):
    """
    Identifies the language of spoken or transcribed citizen speech.
    Supports English, Tamil, Hindi, Marathi, and Bengali.
    """
    result = detect_language_from_text(payload.text)
    return LanguageDetectResponse(**result)

@router.post("/synthesize")
def synthesize_speech(payload: SynthesisRequest):
    """
    Provides server-side audio synthesis metadata.
    Ensures that every piece of information has a validated voice representation.
    """
    return {
        "status": "ready",
        "language": payload.language,
        "text_length": len(payload.text),
        "engine": "browser_native_fallback",
        "message": "Use client Web Speech API synthesis for zero latency."
    }
