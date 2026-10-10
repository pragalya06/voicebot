from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.rag_service import rag_service
from app.data.schemes_data import VERIFIED_SCHEMES

router = APIRouter(prefix="/api/assistant", tags=["Assistant & RAG Q&A"])

class AskRequest(BaseModel):
    query: str
    language: str = "ta" # "ta" or "en"

class AskResponse(BaseModel):
    matched: bool
    is_clarification: bool = False
    clarification_options: Optional[List[Dict[str, str]]] = None
    query: str
    language: str
    scheme_id: Optional[str] = None
    scheme_name: Optional[str] = None
    answer: str
    voice_summary: str
    benefit: Optional[str] = None
    eligibility_rules: Optional[List[str]] = None
    required_documents: Optional[List[str]] = None
    application_steps: Optional[List[str]] = None
    source_name: str
    source_portal: str
    disclaimer: str

@router.post("/ask", response_model=AskResponse)
def ask_assistant(payload: AskRequest):
    """
    RAG-grounded Assistant Endpoint.
    1. Checks if question is vague and needs polite clarification.
    2. Retrieves verified scheme facts via RAG service.
    3. Returns citations, official links, and voice-ready summaries.
    """
    query_clean = payload.query.strip().lower()
    is_tamil = (payload.language == "ta")

    # Ambiguity detection: If user input is too brief or ambiguous, trigger clarification flow
    vague_terms = ["help", "pension", "scheme", "உதவி", "திட்டம்", "ஓய்வூதியம்"]
    if query_clean in vague_terms or len(query_clean.split()) == 1 and query_clean in vague_terms:
        if "pension" in query_clean or "ஓய்வூதியம்" in query_clean:
            return AskResponse(
                matched=True,
                is_clarification=True,
                clarification_options=[
                    {
                        "label": "முதியோர் ஓய்வூதிய தகுதி அறிய" if is_tamil else "Check Old Age Pension Eligibility",
                        "query": "முதியோர் ஓய்வூதிய தகுதி வரம்புகள்" if is_tamil else "Old Age Pension eligibility criteria"
                    },
                    {
                        "label": "விதவை ஓய்வூதியம் பற்றி அறிய" if is_tamil else "Check Destitute Widow Pension",
                        "query": "ஆதரவற்ற விதவை ஓய்வூதியம்" if is_tamil else "Destitute widow pension details"
                    },
                    {
                        "label": "ஓய்வூதிய விண்ணப்ப ஆவணங்கள்" if is_tamil else "Required Documents for Pension",
                        "query": "ஓய்வூதியத்திற்கு என்னென்ன ஆவணங்கள் தேவை" if is_tamil else "What documents are needed for pension"
                    }
                ],
                query=payload.query,
                language=payload.language,
                answer=(
                    "நீங்கள் ஓய்வூதியம் பற்றி கேட்கிறீர்கள். நீங்கள் முதியோர் ஓய்வூதியம் பற்றி அறிய விரும்புகிறீர்களா அல்லது விதவை ஓய்வூதியம் பற்றி அறிய விரும்புகிறீர்களா?"
                    if is_tamil else
                    "You asked about pension. Are you asking about Old Age Pension eligibility, Widow Pension, or required documents?"
                ),
                voice_summary=(
                    "நீங்கள் முதியோர் ஓய்வூதியத்தை கேட்கிறீர்களா அல்லது விதவை ஓய்வூதியத்தை கேட்கிறீர்களா?"
                    if is_tamil else
                    "Are you asking about Old Age Pension or Widow Pension?"
                ),
                source_name="Tamil Nadu Social Welfare Dept",
                source_portal="https://tn.gov.in",
                disclaimer="Clarification prompt to ensure accurate assistance."
            )

    # Perform RAG retrieval
    result = rag_service.answer_query(payload.query, lang=payload.language)

    return AskResponse(
        matched=result["matched"],
        is_clarification=False,
        query=result["query"],
        language=result["language"],
        scheme_id=result.get("scheme_id"),
        scheme_name=result.get("scheme_name"),
        answer=result["answer"],
        voice_summary=result["voice_summary"],
        benefit=result.get("benefit"),
        eligibility_rules=result.get("eligibility_rules"),
        required_documents=result.get("required_documents"),
        application_steps=result.get("application_steps"),
        source_name=result["source_name"],
        source_portal=result["source_portal"],
        disclaimer=result["disclaimer"]
    )

@router.get("/schemes")
def list_verified_schemes(lang: str = "ta"):
    """Returns catalog of all verified government schemes."""
    is_tamil = (lang == "ta")
    return [
        {
            "id": s["id"],
            "name": s["name_ta"] if is_tamil else s["name_en"],
            "category": s["category"],
            "benefit": s["benefit_ta"] if is_tamil else s["benefit_en"],
            "official_portal": s["official_portal"],
            "source_citation": s["official_source_citation"]
        }
        for s in VERIFIED_SCHEMES
    ]
