"""
Assistant API routes.
Improvements:
  1. Language auto-detection: backend detects query language from text, overrides client hint.
  2. General services KB: all queries routed through unified RAG (no topic blocklists).
  3. Session-based conversation context: follow-up resolution and topic-change detection
     using a lightweight in-memory session store with 30-minute TTL.
     - No login or permanent activity tracking.
     - Session data is ephemeral and keyed by a UUID generated on the frontend.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
import time
import re

from app.services.rag_service import rag_service
from app.services.language_detection_service import detect_language_from_text
from app.data.schemes_data import VERIFIED_SCHEMES

router = APIRouter(prefix="/api/assistant", tags=["Assistant & RAG Q&A"])

# ─────────────────────────────────────────────────────────────────────────────
# In-memory session store
# ─────────────────────────────────────────────────────────────────────────────
# Structure:  session_id → SessionData dict
# TTL:        30 minutes from last activity (seconds)
# Max history kept per session: 10 messages (5 exchanges)
# This is NOT persistent storage — no login, no tracking across restarts.

SESSION_TTL_SECONDS = 30 * 60   # 30 minutes
MAX_HISTORY_MESSAGES = 10       # 5 user + 5 assistant

_SESSIONS: Dict[str, Dict] = {}


def _get_or_create_session(session_id: Optional[str]) -> tuple[str, Dict]:
    """
    Returns (canonical_session_id, session_data).
    Creates a fresh session if session_id is None, empty, or expired.
    """
    now = time.monotonic()

    # Validate incoming session_id
    if session_id and session_id in _SESSIONS:
        sess = _SESSIONS[session_id]
        if now - sess["last_active"] < SESSION_TTL_SECONDS:
            sess["last_active"] = now
            return session_id, sess
        # Expired — clean up and create fresh
        del _SESSIONS[session_id]

    # Create new session
    new_id = str(uuid.uuid4())
    _SESSIONS[new_id] = {
        "last_active": now,
        "last_topic_id": None,        # id of last matched service/scheme
        "last_topic_name": None,      # human-readable name
        "last_topic_type": None,      # 'scheme' | 'service'
        "history": [],                # list of {"role": "user"|"assistant", "content": str}
    }
    return new_id, _SESSIONS[new_id]


def _push_history(sess: Dict, user_msg: str, assistant_msg: str) -> None:
    """Appends a user+assistant exchange to the session history, capping at MAX_HISTORY_MESSAGES."""
    sess["history"].append({"role": "user", "content": user_msg})
    sess["history"].append({"role": "assistant", "content": assistant_msg})
    # Trim oldest messages when over limit
    if len(sess["history"]) > MAX_HISTORY_MESSAGES:
        sess["history"] = sess["history"][-MAX_HISTORY_MESSAGES:]


def _prune_expired_sessions() -> None:
    """Evict sessions that have exceeded the TTL. Called occasionally."""
    now = time.monotonic()
    expired = [sid for sid, s in _SESSIONS.items()
               if now - s["last_active"] >= SESSION_TTL_SECONDS]
    for sid in expired:
        del _SESSIONS[sid]


# ─────────────────────────────────────────────────────────────────────────────
# Follow-up / topic-change detection
# ─────────────────────────────────────────────────────────────────────────────

# Words / phrases that indicate the user is referring back to the previous topic
_FOLLOWUP_SIGNALS = {
    # English
    "it", "its", "this", "that", "these", "those", "the scheme", "the service",
    "documents", "document", "fees", "fee", "cost", "costs", "price",
    "how much", "how long", "how many", "processing time", "time taken",
    "next step", "next steps", "what else", "anything else", "more details",
    "apply", "application", "eligibility", "eligible", "qualify", "process",
    "same", "above", "mentioned", "requirements", "criteria", "rules",
    # Tamil
    "இதற்கு", "அதற்கு", "இந்த", "அந்த", "ஆவணங்கள்", "ஆவணம்", "கட்டணம்", "எவ்வளவு",
    "எத்தனை", "எப்போது", "மேலும்", "அடுத்து", "படிவம்", "தகுதி", "நாட்கள்", "தேவை",
    # Hindi
    "इसके", "उसके", "इसमें", "इससे", "यह", "वह", "दस्तावेज", "कागजात", "कागज़ात",
    "फीस", "शुल्क", "कितना", "कितने", "कब", "आगे", "पात्रता", "नियम", "समय", "चाहिए",
    "लाभ", "फायदे", "पैसे", "रुपये", "किस्त", "आवेदन",
    # Marathi
    "याचे", "त्याचे", "यात", "यामध्ये", "याचा", "याची", "यासाठी", "कागदपत्रे",
    "शुल्क", "किती", "केव्हा", "पुढे", "पात्रता", "अटी", "वेळ", "लागेल",
    "लाभ", "फायदे", "पैसे", "रुपये", "हप्ता", "अर्ज",
    # Bengali
    "এর", "এই", "সেই", "এতে", "নথিপত্র", "কাগজপত্র", "ফি", "কত", "কখন", "আরও",
    "যোগ্যতা", "নিয়ম", "সময়", "লাগবে", "সুবিধা", "টাকা", "কিস্তি", "আবেদন",
}

# Words that strongly indicate a NEW independent topic (not a follow-up)
_NEW_TOPIC_SIGNALS = {
    # English
    "passport", "pan card", "pan", "aadhaar", "aadhar", "driving licence",
    "driving license", "dl", "rto", "birth certificate", "death certificate",
    "voter id", "voter card", "epic", "ration card", "family card", "smart card",
    "income certificate", "caste certificate", "community certificate",
    "scholarship", "scholarships", "complaint", "grievance", "cpgrams", "1100",
    "delayed application", "correction", "name correction", "dob correction",
    "ayushman", "pmjay", "pension", "old age pension", "widow pension",
    "kisan", "pm-kisan", "pm kisan", "pmkisan", "magalir", "cmchis", "health insurance", "widow",

    # Tamil
    "பாஸ்போர்ட்", "பான்", "பான் கார்டு", "பான் அட்டை", "ஆதார்", "ஆதார் அட்டை",
    "ஓட்டுனர்", "ஓட்டுனர் உரிமம்", "கற்றல் உரிமம்", "பிறப்பு", "பிறப்புச் சான்றிதழ்",
    "இறப்பு", "இறப்புச் சான்றிதழ்", "மரண", "வாக்காளர்", "வாக்காளர் அட்டை",
    "ரேஷன்", "ரேஷன் கார்டு", "குடும்ப அட்டை", "ஸ்மார்ட் கார்டு",
    "வருமானம்", "வருமானச் சான்றிதழ்", "சாதி", "சாதிச் சான்றிதழ்",
    "உதவித்தொகை", "கல்வி உதவித்தொகை", "ஸ்காலர்ஷிப்",
    "புகார்", "குறைதீர்ப்பு", "மனு", "முதல்வர் உதவி",
    "திருத்தம்", "பெயர் மாற்றம்", "பிறந்த தேதி மாற்றம்",
    "ஓய்வூதியம்", "முதியோர்", "விதவை", "கிசான்", "பிஎம் கிசான்", "விவசாயி", "மகளிர்", "காப்பீடு", "ஆயுஷ்மான்",

    # Hindi
    "पासपोर्ट", "पैन", "पैन कार्ड", "आधार", "आधार कार्ड",
    "ड्राइविंग", "ड्राइविंग लाइसेंस", "चालक", "जन्म", "जन्म प्रमाण",
    "मृत्यु", "मृत्यु प्रमाण", "मतदाता", "वोटर आईडी", "पहचान पत्र",
    "राशन", "राशन कार्ड", "आय प्रमाण", "जाति प्रमाण",
    "छात्रवृत्ति", "स्कॉलरशिप", "शिकायत", "जनसुनवाई", "सुधार", "नाम सुधार",
    "पेंशन", "वृद्धावस्था", "विधवा", "किसान", "पीएम किसान", "पीएम-किसान", "पीएमकिसान",
    "किसान सम्मान निधि", "आयुष्मान", "स्वास्थ्य बीमा",

    # Marathi
    "पॅन", "पॅन कार्ड", "वाहन चालक", "परवाना", "जन्म दाखला", "मृत्यू दाखला",
    "मतदार", "मतदार ओळखपत्र", "रेशन", "रेशन कार्ड", "उत्पन्न दाखला", "जात प्रमाणपत्र",
    "शिष्यवृत्ती", "तक्रार", "दुरुस्ती", "पेन्शन", "शेतकरी", "पीएम किसान", "शेतकरी सन्मान निधी",
    "शेतकरी योजना", "शेती योजना", "आरोग्य विमा",

    # Bengali
    "পাসপোর্ট", "প্যান", "প্যান কার্ড", "আধার", "ড্রাইভিং লাইসেন্স",
    "জন্ম সনদ", "মৃত্যু সনদ", "ভোটার", "ভোটার কার্ড", "রেশন", "রেশন কার্ড",
    "আয়ের শংসাপত্র", "জাতিগত শংসাপত্র", "স্কলারশিপ", "বৃত্তি",
    "অভিযোগ", "সংশোধন", "পেনশন", "কৃষক", "পিএম কিষাণ", "পিএম কিষান", "কৃষক সম্মান নিধি", "আয়ুষ্মান",
}


def _resolve_query_with_context(query: str, sess: Dict) -> str:
    """
    If the query looks like a genuine follow-up (contains follow-up signals or attribute
    questions without any new topic signals), enrich it with the prior topic.
    If the query mentions a new service or topic, or does not ask about prior topic
    attributes, treat it as a fresh query without prior topic poisoning.
    """
    if not sess["last_topic_id"]:
        return query  # No prior context — use as-is

    q_lower = query.strip().lower()
    words = set(re.split(r'[\s,?.!;:\u0964\u0965]+', q_lower))

    # Check for explicit new-topic mention
    for signal in _NEW_TOPIC_SIGNALS:
        if re.search(r'(?<!\w)' + re.escape(signal) + r'(?!\w)', q_lower) or signal in q_lower:
            return query

    # Check for genuine follow-up signals
    has_followup = bool(words.intersection(_FOLLOWUP_SIGNALS))

    if has_followup:
        # Genuine follow-up referring to the prior topic
        enriched = f"{sess['last_topic_name']} {query}"
        return enriched

    return query


def _detect_language_server_side(text: str, client_lang: str) -> str:
    """
    Uses Unicode script and lexical analysis to detect the language of the query text.
    If detection confidence is high (>= 0.80), trusts the detected language.
    Falls back to client_lang for ambiguous Latin text.
    """
    result = detect_language_from_text(text)
    if not result.get("is_uncertain") and result.get("confidence", 0) >= 0.80:
        return result["detected_language"]
    return client_lang  # Trust client hint for ambiguous (Latin-script) input


# ─────────────────────────────────────────────────────────────────────────────
# Request / Response models
# ─────────────────────────────────────────────────────────────────────────────

class ConversationMessage(BaseModel):
    role: str   # "user" | "assistant"
    content: str


class AskRequest(BaseModel):
    query: str
    language: str = "en"
    session_id: Optional[str] = Field(default=None, max_length=64)
    # Client sends last N exchanges so the server can validate / supplement
    conversation_history: Optional[List[ConversationMessage]] = Field(default=None, max_items=10)


class AskResponse(BaseModel):
    matched: bool
    is_clarification: bool = False
    clarification_options: Optional[List[Dict[str, str]]] = None
    query: str
    language: str
    session_id: str
    scheme_id: Optional[str] = None
    scheme_name: Optional[str] = None
    service_type: Optional[str] = None
    answer: str
    voice_summary: str
    benefit: Optional[str] = None
    eligibility_rules: Optional[List[str]] = None
    required_documents: Optional[List[str]] = None
    application_steps: Optional[List[str]] = None
    source_name: str
    source_portal: str
    disclaimer: str


# ─────────────────────────────────────────────────────────────────────────────
# Clarification helpers (vague single-word queries)
# ─────────────────────────────────────────────────────────────────────────────

_VAGUE_TERMS = {
    "help", "scheme", "schemes", "yojana", "தொகை", "திட்டம்", "উপায়",
    "service", "services", "information", "info", "details",
}

_PENSION_TERMS = {"pension", "ஓய்வூதியம்", "पेंशन", "পেনশন", "पेन्शन"}


def _maybe_clarify(query_clean: str, lang: str) -> Optional[AskResponse]:
    """
    Returns a clarification AskResponse for genuinely vague single-word queries,
    or None if the query is specific enough to route to RAG.
    """
    tokens = query_clean.strip().split()

    # Only intercept vague single/double-word queries
    if len(tokens) > 2:
        return None
    if query_clean not in _VAGUE_TERMS and not tokens[0] in _VAGUE_TERMS:
        return None

    # Pension disambiguation
    if any(t in query_clean for t in _PENSION_TERMS):
        opts_en = [
            {"label": "Old Age Pension (60+ years)", "query": "Old Age Pension eligibility and documents"},
            {"label": "Destitute Widow Pension", "query": "Widow pension eligibility and documents"},
            {"label": "Documents needed for pension", "query": "What documents are needed for pension application"},
        ]
        opts_ta = [
            {"label": "முதியோர் ஓய்வூதியம் (60+ வயது)", "query": "முதியோர் ஓய்வூதிய தகுதி மற்றும் ஆவணங்கள்"},
            {"label": "ஆதரவற்ற விதவை ஓய்வூதியம்", "query": "விதவை ஓய்வூதிய தகுதி மற்றும் ஆவணங்கள்"},
            {"label": "ஓய்வூதியத்திற்கு தேவையான ஆவணங்கள்", "query": "ஓய்வூதியத்திற்கு என்னென்ன ஆவணங்கள் தேவை"},
        ]
        opts_hi = [
            {"label": "वृद्धावस्था पेंशन (60+ वर्ष)", "query": "वृद्धावस्था पेंशन पात्रता और दस्तावेज"},
            {"label": "निराश्रित विधवा पेंशन", "query": "विधवा पेंशन पात्रता और दस्तावेज"},
            {"label": "पेंशन के लिए आवश्यक दस्तावेज", "query": "पेंशन के लिए कौन से दस्तावेज चाहिए"},
        ]
        opts_mr = [
            {"label": "वृद्धापकाळ पेन्शन (६०+ वर्षे)", "query": "वृद्धापकाळ पेन्शन पात्रता आणि कागदपत्रे"},
            {"label": "निराधार विधवा पेन्शन", "query": "विधवा पेन्शन पात्रता आणि कागदपत्रे"},
            {"label": "पेन्शनसाठी आवश्यक कागदपत्रे", "query": "पेन्शनसाठी कोणती कागदपत्रे लागतील"},
        ]
        opts_bn = [
            {"label": "বার্ধক্য পেনশন (৬০+ বছর)", "query": "বার্ধক্য পেনশন যোগ্যতা এবং নথিপত্র"},
            {"label": "নিরাশ্রয় বিধবা পেনশন", "query": "বিধবা পেনশন যোগ্যতা এবং নথিপত্র"},
            {"label": "পেনশনের জন্য প্রয়োজনীয় কাগজপত্র", "query": "পেনশনের জন্য কী কী কাগজপত্র প্রয়োজন"},
        ]
        opts_map = {"ta": opts_ta, "hi": opts_hi, "mr": opts_mr, "bn": opts_bn, "en": opts_en}
        opts = opts_map.get(lang, opts_en)
        questions = {
            "ta": "நீங்கள் எந்த ஓய்வூதிய திட்டம் பற்றி அறிய விரும்புகிறீர்கள்?",
            "hi": "आप किस पेंशन योजना के बारे में जानना चाहते हैं?",
            "mr": "तुम्हाला कोणत्या पेन्शन योजनेबद्दल माहिती हवी आहे?",
            "bn": "আপনি কোন পেনশন প্রকল্প সম্পর্কে জানতে চান?",
            "en": "Which pension scheme would you like to know about?",
        }
        q_text = questions.get(lang, questions["en"])
        # This is a partial return — caller must supply session_id
        return {
            "matched": True,
            "is_clarification": True,
            "clarification_options": opts,
            "answer": q_text,
            "voice_summary": q_text,
            "source_name": "SevaMitra Assistant",
            "source_portal": "https://tn.gov.in",
            "disclaimer": "Clarification prompt.",
        }

    return None


# ─────────────────────────────────────────────────────────────────────────────
# Main endpoint
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/ask", response_model=AskResponse)
def ask_assistant(payload: AskRequest):
    """
    Unified assistant endpoint.
    Flow:
      1. Get/create session.
      2. Server-side language detection from query text.
      3. Resolve follow-up queries using session context.
      4. RAG retrieval across welfare schemes + general services.
      5. Update session with new topic + history.
      6. Return grounded, source-traceable answer.
    """
    # Occasional housekeeping
    if len(_SESSIONS) > 500:
        _prune_expired_sessions()

    # 1. Session management
    session_id, sess = _get_or_create_session(payload.session_id)

    # 2. Server-side language detection (overrides client hint for non-Latin scripts)
    detected_lang = _detect_language_server_side(payload.query, payload.language)

    query_clean = payload.query.strip()

    # 3. Clarification for vague single-word queries
    clarify = _maybe_clarify(query_clean.lower(), detected_lang)
    if clarify:
        return AskResponse(
            session_id=session_id,
            query=query_clean,
            language=detected_lang,
            scheme_id=None,
            scheme_name=None,
            service_type=None,
            eligibility_rules=None,
            required_documents=None,
            application_steps=None,
            benefit=None,
            **clarify,
        )

    # 4. Resolve follow-ups by enriching query with prior topic context
    enriched_query = _resolve_query_with_context(query_clean, sess)

    # 5. RAG retrieval
    result = rag_service.answer_query(enriched_query, lang=detected_lang)

    # 6. Update session context
    if result.get("matched"):
        sess["last_topic_id"] = result.get("scheme_id")
        sess["last_topic_name"] = result.get("scheme_name")
        sess["last_topic_type"] = result.get("service_type")

    _push_history(sess, query_clean, result.get("answer", ""))

    return AskResponse(
        matched=result["matched"],
        is_clarification=False,
        query=result["query"],
        language=result["language"],
        session_id=session_id,
        scheme_id=result.get("scheme_id"),
        scheme_name=result.get("scheme_name"),
        service_type=result.get("service_type"),
        answer=result["answer"],
        voice_summary=result["voice_summary"],
        benefit=result.get("benefit"),
        eligibility_rules=result.get("eligibility_rules"),
        required_documents=result.get("required_documents"),
        application_steps=result.get("application_steps"),
        source_name=result["source_name"],
        source_portal=result["source_portal"],
        disclaimer=result["disclaimer"],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Schemes catalogue
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/schemes")
def list_verified_schemes(lang: str = "en"):
    """Returns catalogue of all verified government welfare schemes in the requested language."""
    return [
        {
            "id": s["id"],
            "name": s.get(f"name_{lang}") or s.get("name_en"),
            "category": s["category"],
            "benefit": s.get(f"benefit_{lang}") or s.get("benefit_en"),
            "official_portal": s["official_portal"],
            "source_citation": s["official_source_citation"],
        }
        for s in VERIFIED_SCHEMES
    ]

