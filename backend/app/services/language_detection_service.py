"""
Language Detection Service: Identifies spoken and written Indian languages
(Tamil, English, Hindi, Marathi, Bengali) using script analysis, lexical markers,
and grammatical disambiguation.
"""

import re
from typing import Dict, Any, Optional

# Catalog of supported languages
SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "ta": {"name": "Tamil", "native": "தமிழ்", "flag": "🇮🇳", "speech_locale": "ta-IN"},
    "en": {"name": "English", "native": "English", "flag": "🌐", "speech_locale": "en-IN"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "flag": "🇮🇳", "speech_locale": "hi-IN"},
    "mr": {"name": "Marathi", "native": "मराठी", "flag": "🇮🇳", "speech_locale": "mr-IN"},
    "bn": {"name": "Bengali", "native": "বাংলা", "flag": "🇮🇳", "speech_locale": "bn-IN"},
}

# Distinct lexical markers for Marathi
MARATHI_MARKERS = {
    "आहे", "आहेत", "नाही", "नाहीत", "होते", "होती", "शेतकरी", "माहिती", "कसे", "कशी",
    "कसा", "काय", "अर्ज", "मिळेल", "मिळतात", "करायचे", "केले", "झाले", "वय", "पाहिजे",
    "शासन", "गावात", "योजनेचा", "योजनेची", "योजनेचे", "तपशील", "कागदपत्रे", "दाखला",
    "परवाना", "तक्रार", "नूतनीकरण", "दुरुस्ती", "नाव", "पत्ता", "नोंदणी", "करावी",
    "करावे", "करावा", "लागेल", "शकतो", "शकते", "हवे", "हवी", "द्यावे", "घ्यावे",
    "यांचे", "त्यांचे", "आमचे", "तुमचे", "मध्ये", "वरून", "साठी", "पासून", "पर्यंत",
    "बदल", "काढावा", "काढावे", "काढायचा", "पॅन"
}

# Distinct lexical markers for Hindi
HINDI_MARKERS = {
    "है", "हैं", "नहीं", "था", "थी", "थे", "किसान", "जानकारी", "कैसे", "क्या",
    "आवेदन", "मिलेगा", "मिलता", "करना", "किया", "गया", "उम्र", "चाहिए", "सरकार",
    "गाँव", "गांव", "योजना", "दस्तावेज", "प्रमाण", "पत्र", "लाइसेंस", "शिकायत",
    "सुधार", "नाम", "पता", "पंजीकरण", "नवीनीकरण", "होगा", "सकता", "सकती", "सकते",
    "देना", "लेना", "इनका", "उनका", "हमारा", "आपका", "में", "से", "तक", "बदलना",
    "बनवाना", "चाहता", "चाहती", "पैन"
}

# Romanized keyword markers (strictly conversational / grammatical words, not scheme or entity nouns)
ROMANIZED_TAMIL = {"vanakkam", "thittam", "oivuthiyam", "vivasayi", "magalir", "eppadi", "thevai", "katnam", "ungalukku", "enakku"}
ROMANIZED_HINDI = {"namaste", "kaise", "kya", "aavedan", "chahiye", "dastavej", "batao", "mujhe", "kripya", "hoga", "karna"}
ROMANIZED_MARATHI = {"namaskar", "shetkari", "mahiti", "kasa", "kashi", "kay", "arja", "pahije", "kagadpatre", "sangitla"}
ROMANIZED_BENGALI = {"nomoshkar", "krishok", "kivabe", "taka", "dorar", "bolun", "amake", "chai"}

# Common English grammatical and functional words
ENGLISH_WORDS = {
    "what", "is", "are", "how", "to", "apply", "for", "tell", "me", "about",
    "can", "i", "get", "details", "eligibility", "documents", "scheme", "benefits",
    "who", "which", "where", "when", "why", "do", "does", "did", "have", "has",
    "the", "a", "an", "in", "of", "and", "or", "my", "your", "information", "help",
    "need", "want", "know", "please", "status", "card", "certificate", "procedure",
    "under", "online", "portal", "official", "rules", "guidelines", "register"
}


def detect_language_from_text(text: str) -> Dict[str, Any]:
    """
    Analyzes input text to identify the language code (ta, en, hi, mr, bn)
    and confidence level.
    """
    clean_text = (text or "").strip()
    if not clean_text:
        return {
            "detected_language": "en",
            "language_name": "English",
            "native_name": "English",
            "flag": "🌐",
            "speech_locale": "en-IN",
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
    if tamil_chars > 0 and tamil_chars >= (bengali_chars + devanagari_chars + latin_chars * 0.4):
        confidence = min(0.98, 0.75 + (tamil_chars / max(total_relevant, 1)) * 0.25)
        return _format_result("ta", confidence, "Tamil")

    # 2. Clear Bengali Script match
    if bengali_chars > 0 and bengali_chars >= (tamil_chars + devanagari_chars + latin_chars * 0.4):
        confidence = min(0.98, 0.75 + (bengali_chars / max(total_relevant, 1)) * 0.25)
        return _format_result("bn", confidence, "Bengali")

    # 3. Devanagari Script (Disambiguate Hindi vs Marathi)
    if devanagari_chars > 0 and devanagari_chars >= (tamil_chars + bengali_chars):
        # A. Check for character 'ळ' (U+0933) which exists exclusively in Marathi
        if 'ळ' in clean_text:
            return _format_result("mr", 0.98, "Devanagari (Marathi)")

        words = set(re.split(r"[\s,?.!;:'\"/\\।॥]+", clean_text))
        marathi_hits = len(words.intersection(MARATHI_MARKERS))
        hindi_hits = len(words.intersection(HINDI_MARKERS))

        if marathi_hits > hindi_hits:
            confidence = min(0.96, 0.82 + (marathi_hits * 0.05))
            return _format_result("mr", confidence, "Devanagari (Marathi)")
        elif hindi_hits > marathi_hits:
            confidence = min(0.96, 0.82 + (hindi_hits * 0.05))
            return _format_result("hi", confidence, "Devanagari (Hindi)")
        else:
            # Check distinctive auxiliary verbs
            if any(w in words for w in ["आहे", "नाही", "कसे", "कशी", "काय"]):
                return _format_result("mr", 0.92, "Devanagari (Marathi)")
            if any(w in words for w in ["है", "हैं", "नहीं", "कैसे", "क्या", "चाहिए"]):
                return _format_result("hi", 0.92, "Devanagari (Hindi)")

            # Default Devanagari to Hindi
            return _format_result("hi", 0.85, "Devanagari (Hindi)")

    # 4. Latin / English / Romanized
    words_lower = set(re.findall(r'\b[a-zA-Z]+\b', clean_text.lower()))
    english_hits = len(words_lower.intersection(ENGLISH_WORDS))

    # Calculate Romanized matches
    ta_hits = len(words_lower.intersection(ROMANIZED_TAMIL))
    hi_hits = len(words_lower.intersection(ROMANIZED_HINDI))
    mr_hits = len(words_lower.intersection(ROMANIZED_MARATHI))
    bn_hits = len(words_lower.intersection(ROMANIZED_BENGALI))

    # If sentence contains English grammatical words, it is English (e.g. "What is PM-KISAN?")
    if english_hits >= 1 and english_hits >= max(ta_hits, hi_hits, mr_hits, bn_hits):
        return _format_result("en", 0.95, "English")

    # Check for Romanized Indian words when English grammar is not dominant
    if hi_hits > english_hits and hi_hits >= max(ta_hits, mr_hits, bn_hits):
        return _format_result("hi", 0.90, "Romanized Hindi")
    if ta_hits > english_hits and ta_hits >= max(hi_hits, mr_hits, bn_hits):
        return _format_result("ta", 0.90, "Romanized Tamil")
    if mr_hits > english_hits and mr_hits >= max(ta_hits, hi_hits, bn_hits):
        return _format_result("mr", 0.90, "Romanized Marathi")
    if bn_hits > english_hits and bn_hits >= max(ta_hits, hi_hits, mr_hits):
        return _format_result("bn", 0.90, "Romanized Bengali")

    # Default pure Latin text to English
    return _format_result("en", 0.95, "English")


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
