"""
Language Detection Service: Identifies spoken and written Indian languages
(Tamil, English, Hindi, Marathi, Bengali) using script analysis, lexical markers,
and Bhashini LID compatibility with confidence scoring and fallback handling.
"""

import re
from typing import Dict, Any, Tuple, Optional

# Catalog of supported languages
SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "ta": {"name": "Tamil", "native": "தமிழ்", "flag": "🇮🇳", "speech_locale": "ta-IN"},
    "en": {"name": "English", "native": "English", "flag": "🌐", "speech_locale": "en-IN"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "flag": "🇮🇳", "speech_locale": "hi-IN"},
    "mr": {"name": "Marathi", "native": "मराठी", "flag": "🇮🇳", "speech_locale": "mr-IN"},
    "bn": {"name": "Bengali", "native": "বাংলা", "flag": "🇮🇳", "speech_locale": "bn-IN"},
}

# Lexical markers for disambiguation
MARATHI_MARKERS = {
    "आहे", "नाही", "शेतकरी", "माहिती", "कसे", "काय", "अर्ज", "मिळेल",
    "करायचे", "केले", "झाले", "वय", "पाहिजे", "शासन", "गावात", "योजनेचा"
}

HINDI_MARKERS = {
    "है", "नहीं", "किसान", "जानकारी", "कैसे", "क्या", "आवेदन", "मिलेगा",
    "करना", "किया", "गया", "उम्र", "चाहिए", "सरकार", "गाँव", "योजना"
}

TAMIL_MARKERS = {
    "திட்டம்", "ஓய்வூதியம்", "விவசாயி", "மகளிர்", "எப்படி", "விண்ணப்பிக்க",
    "தகுதி", "ஆவணம்", "அரசு", "உதவி", "பணம்", "ஆதார்", "குடும்ப", "அட்டை"
}

BENGALI_MARKERS = {
    "যোজনা", "পেনশন", "কৃষক", "আবেদন", "কিভাবে", "কি", "যোগ্যতা", "নথি",
    "টাকা", "সরকার", "সাহায্য", "আধার", "কার্ড"
}

# Romanized keyword markers
ROMANIZED_TAMIL = {"vanakkam", "thittam", "oivuthiyam", "vivasayi", "magalir", "eppadi", "aadhaar"}
ROMANIZED_HINDI = {"namaste", "yojana", "pension", "kisan", "kaise", "kya", "aavedan", "aadhaar"}
ROMANIZED_MARATHI = {"namaskar", "yojana", "shetkari", "mahiti", "kasa", "kay", "arja"}
ROMANIZED_BENGALI = {"nomoshkar", "jojona", "prokolpo", "krishok", "kivabe", "taka"}

def detect_language_from_text(text: str) -> Dict[str, Any]:
    """
    Analyzes input text to identify the spoken language code and confidence level.
    Supports native scripts (Tamil, Devanagari, Bengali) and transliterated Latin input.
    """
    clean_text = (text or "").strip()
    if not clean_text:
        return {
            "detected_language": "en",
            "language_name": "English",
            "native_name": "English",
            "confidence": 0.0,
            "is_supported": True,
            "is_uncertain": True,
            "message": "Empty speech or text provided."
        }

    # Count script characters
    tamil_chars = len(re.findall(r'[\u0B80-\u0BFF]', clean_text))
    bengali_chars = len(re.findall(r'[\u0980-\u09FF]', clean_text))
    devanagari_chars = len(re.findall(r'[\u0900-\u097F]', clean_text))
    latin_chars = len(re.findall(r'[a-zA-Z]', clean_text))
    total_relevant = tamil_chars + bengali_chars + devanagari_chars + latin_chars

    # 1. Clear Tamil Script match
    if tamil_chars > 0 and tamil_chars >= (bengali_chars + devanagari_chars + latin_chars * 0.5):
        confidence = min(0.98, 0.7 + (tamil_chars / max(total_relevant, 1)) * 0.3)
        return _format_result("ta", confidence, "Tamil")

    # 2. Clear Bengali Script match
    if bengali_chars > 0 and bengali_chars >= (tamil_chars + devanagari_chars + latin_chars * 0.5):
        confidence = min(0.98, 0.7 + (bengali_chars / max(total_relevant, 1)) * 0.3)
        return _format_result("bn", confidence, "Bengali")

    # 3. Devanagari Script (Disambiguate Hindi vs Marathi)
    if devanagari_chars > 0 and devanagari_chars >= (tamil_chars + bengali_chars):
        words = set(clean_text.split())
        marathi_hits = len(words.intersection(MARATHI_MARKERS))
        hindi_hits = len(words.intersection(HINDI_MARKERS))

        if marathi_hits > hindi_hits:
            confidence = min(0.96, 0.8 + (marathi_hits * 0.05))
            return _format_result("mr", confidence, "Devanagari (Marathi)")
        elif hindi_hits > 0 or ("ह" in clean_text or "है" in clean_text):
            confidence = min(0.96, 0.8 + (hindi_hits * 0.05))
            return _format_result("hi", confidence, "Devanagari (Hindi)")
        else:
            # Default to Hindi for general Devanagari with slight uncertainty flag
            return _format_result("hi", 0.85, "Devanagari")

    # 4. Latin / English / Romanized Indian speech
    words_lower = set(re.findall(r'\b[a-zA-Z]+\b', clean_text.lower()))

    # English grammatical / structural markers
    english_structural = {"how", "can", "i", "apply", "for", "the", "what", "is", "tell", "me", "about", "who", "where", "my", "eligible"}
    english_hits = len(words_lower.intersection(english_structural))

    if english_hits >= 2:
        confidence = min(0.96, 0.75 + (english_hits * 0.05))
        return _format_result("en", confidence, "English")

    # Check for Romanized Indian words
    if words_lower.intersection(ROMANIZED_TAMIL):
        return _format_result("ta", 0.88, "Romanized Tamil")
    if words_lower.intersection(ROMANIZED_HINDI):
        return _format_result("hi", 0.88, "Romanized Hindi")
    if words_lower.intersection(ROMANIZED_MARATHI):
        return _format_result("mr", 0.88, "Romanized Marathi")
    if words_lower.intersection(ROMANIZED_BENGALI):
        return _format_result("bn", 0.88, "Romanized Bengali")

    # Default Latin to English
    confidence = min(0.95, 0.75 + (english_hits * 0.05)) if english_hits > 0 else 0.70
    return _format_result("en", confidence, "English")

def _format_result(lang_code: str, confidence: float, script_name: str) -> Dict[str, Any]:
    info = SUPPORTED_LANGUAGES.get(lang_code, SUPPORTED_LANGUAGES["en"])
    is_uncertain = confidence < 0.75
    return {
        "detected_language": lang_code,
        "language_name": info["name"],
        "native_name": info["native"],
        "flag": info["flag"],
        "speech_locale": info["speech_locale"],
        "confidence": round(confidence, 2),
        "is_supported": True,
        "is_uncertain": is_uncertain,
        "script": script_name
    }
