from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.scheme_matcher import match_schemes

router = APIRouter(prefix="/api/schemes", tags=["Scheme Recommendations"])

class CitizenProfileRequest(BaseModel):
    age: int = Field(default=35, ge=1, le=120)
    gender: str = Field(default="female") # "female", "male", "other"
    occupation: str = Field(default="homemaker") # "farmer", "laborer", "homemaker", "salaried", "business"
    annual_income: int = Field(default=48000, ge=0)
    is_rural: bool = Field(default=True)
    has_cultivable_land: bool = Field(default=False)
    marital_status: str = Field(default="married") # "married", "single", "widow"
    language: str = Field(default="ta")

class SchemeMatchCard(BaseModel):
    scheme_id: str
    scheme_name: str
    category: str
    benefit: str
    match_score: int
    status: str
    is_eligible: bool
    why_matched: List[str]
    missing_info: List[str]
    required_documents: List[str]
    official_portal: str
    disclaimer: str

class RecommendationResponse(BaseModel):
    total_evaluated: int
    matched_count: int
    voice_summary: str
    recommendations: List[SchemeMatchCard]

@router.post("/recommend", response_model=RecommendationResponse)
def get_personalized_recommendations(profile: CitizenProfileRequest):
    """
    Evaluates citizen input against verified schemes and returns
    transparent recommendations with match justifications and audio narration summary.
    """
    matches = match_schemes(profile.model_dump(), lang=profile.language)
    is_tamil = (profile.language == "ta")

    high_matches = [m for m in matches if m["match_score"] >= 70]
    matched_names = [m["scheme_name"] for m in high_matches[:2]]

    if high_matches:
        if is_tamil:
            names_str = " மற்றும் ".join(matched_names)
            voice_summary = (
                f"உங்கள் விவரங்களின் அடிப்படையில், {len(high_matches)} திட்டங்கள் உங்களுக்கு அதிகம் பொருந்தக்கூடும்: {names_str}. "
                f"தேவையான ஆவணங்களை கீழே உள்ள அட்டவணையில் காண்க."
            )
        else:
            names_str = " and ".join(matched_names)
            voice_summary = (
                f"Based on your profile, {len(high_matches)} schemes appear highly relevant: {names_str}. "
                f"Review required documents and verification steps below."
            )
    else:
        if is_tamil:
            voice_summary = (
                "உங்கள் விவரங்களின் அடிப்படையில் நேரடி தகுதிபெறும் திட்டங்கள் இல்லை. "
                "ஆனால் மருத்துவ காப்பீடு போன்ற பொதுவான நலத்திட்டங்களை கீழே காணலாம்."
            )
        else:
            voice_summary = (
                "No direct high-match schemes found for this exact profile. "
                "However, general health insurance and social welfare schemes are listed below for review."
            )

    return RecommendationResponse(
        total_evaluated=len(matches),
        matched_count=len(high_matches),
        voice_summary=voice_summary,
        recommendations=matches
    )
