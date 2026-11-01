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
    lang = profile.language or "en"

    high_matches = [m for m in matches if m["match_score"] >= 70]
    matched_names = [m["scheme_name"] for m in high_matches[:2]]

    if high_matches:
        if lang == "ta":
            names_str = " மற்றும் ".join(matched_names)
            voice_summary = (
                f"உங்கள் விவரங்களின் அடிப்படையில், {len(high_matches)} திட்டங்கள் உங்களுக்கு அதிகம் பொருந்தக்கூடும்: {names_str}. "
                f"தேவையான ஆவணங்களை கீழே உள்ள அட்டவணையில் காண்க."
            )
        elif lang == "hi":
            names_str = " और ".join(matched_names)
            voice_summary = (
                f"आपके विवरण के आधार पर, {len(high_matches)} योजनाएं आपके लिए अत्यधिक उपयुक्त हैं: {names_str}। "
                f"कृपया नीचे आवश्यक दस्तावेज और पात्रता नियम देखें।"
            )
        elif lang == "mr":
            names_str = " आणि ".join(matched_names)
            voice_summary = (
                f"तुमच्या तपशिलानुसार, {len(high_matches)} योजना तुमच्यासाठी अत्यंत सुसंगत आहेत: {names_str}. "
                f"खाली आवश्यक कागदपत्रे आणि पडताळणी टप्पे तपासा."
            )
        elif lang == "bn":
            names_str = " এবং ".join(matched_names)
            voice_summary = (
                f"আপনার বিবরণের ভিত্তিতে, {len(high_matches)}টি প্রকল্প আপনার জন্য অত্যন্ত উপযুক্ত: {names_str}। "
                f"নিচে প্রয়োজনীয় নথিপত্র এবং যাচাইকরণের ধাপগুলি পর্যালোচনা করুন।"
            )
        else:
            names_str = " and ".join(matched_names)
            voice_summary = (
                f"Based on your profile, {len(high_matches)} schemes appear highly relevant: {names_str}. "
                f"Review required documents and verification steps below."
            )
    else:
        if lang == "ta":
            voice_summary = (
                "உங்கள் விவரங்களின் அடிப்படையில் நேரடி தகுதிபெறும் திட்டங்கள் இல்லை. "
                "ஆனால் மருத்துவ காப்பீடு போன்ற பொதுவான நலத்திட்டங்களை கீழே காணலாம்."
            )
        elif lang == "hi":
            voice_summary = (
                "आपके प्रोफाइल के अनुसार सीधे उच्च-मिलान योजनाएं नहीं मिलीं। "
                "तथापि, सामान्य स्वास्थ्य बीमा और कल्याणकारी योजनाओं की सूची नीचे दी गई है।"
            )
        elif lang == "mr":
            voice_summary = (
                "तुमच्या प्रोफाइलनुसार थेट उच्च-जुळणी योजना आढळल्या नाहीत. "
                "तथापि, खालील सामान्य आरोग्य विमा आणि कल्याणकारी योजनांची पुनरावलोकन करा."
            )
        elif lang == "bn":
            voice_summary = (
                "আপনার প্রোফাইলের জন্য সরাসরি উচ্চ-মিলযুক্ত প্রকল্প পাওয়া যায়নি। "
                "তবে সাধারণ স্বাস্থ্য বীমা ও সামাজিক সুরক্ষা প্রকল্পগুলি নিচে দেওয়া হয়েছে।"
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
