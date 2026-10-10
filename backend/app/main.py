from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes_speech import router as speech_router
from app.api.routes_assistant import router as assistant_router
from app.api.routes_schemes import router as schemes_router
from app.api.routes_documents import router as documents_router
from app.api.routes_checklist import router as checklist_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for AI-Powered Multilingual Government Service Assistant"
)

# Register Sub-Routers
app.include_router(speech_router)
app.include_router(assistant_router)
app.include_router(schemes_router)
app.include_router(documents_router)
app.include_router(checklist_router)

# Enable Cross-Origin Resource Sharing (CORS) so the React frontend can call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Root route returning API overview."""
    return {
        "message": "Welcome to the Multilingual Government Service Assistant API",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint to verify backend service readiness."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "speech_engine_ready": True,
        "supported_languages": ["en", "ta", "hi", "mr", "bn"]
    }

@app.get("/api/languages")
def get_supported_languages():
    """Return available languages with their native display labels."""
    return [
        {"code": "en", "name": "English", "native": "English", "flag": "🌐"},
        {"code": "ta", "name": "Tamil", "native": "தமிழ்", "flag": "🇮🇳"},
        {"code": "hi", "name": "Hindi", "native": "हिन्दी", "flag": "🇮🇳"},
        {"code": "mr", "name": "Marathi", "native": "मराठी", "flag": "🇮🇳"},
        {"code": "bn", "name": "Bengali", "native": "বাংলা", "flag": "🇮🇳"}
    ]
