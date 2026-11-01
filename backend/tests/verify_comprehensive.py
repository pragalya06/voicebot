import sys
import os

# Set working directory to backend root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.language_detection_service import detect_language_from_text
from app.services.rag_service import rag_service
from app.api.routes_assistant import _detect_language_server_side, _resolve_query_with_context, _get_or_create_session, _push_history
from app.services.scheme_matcher import match_schemes

def run_tests():
    passed = 0
    total = 0

    def assert_eq(test_name, actual, expected, extra=""):
        nonlocal passed, total
        total += 1
        if actual == expected:
            passed += 1
            print(f"[PASS] {test_name}: {actual} == {expected}")
        else:
            print(f"[FAIL] {test_name}: Got '{actual}', Expected '{expected}' {extra}")

    print("=" * 60)
    print("1. LANGUAGE DETECTION TESTS (ALL 5 LANGUAGES)")
    print("=" * 60)

    # English
    r = detect_language_from_text("How to apply for a fresh passport online?")
    assert_eq("Detect English query", r["detected_language"], "en")

    # Tamil
    r = detect_language_from_text("புதிய பாஸ்போர்ட் எடுப்பது எப்படி?")
    assert_eq("Detect Tamil query", r["detected_language"], "ta")

    # Hindi
    r = detect_language_from_text("नया पैन कार्ड कैसे बनवाएं?")
    assert_eq("Detect Hindi query", r["detected_language"], "hi")

    # Marathi with ळ
    r = detect_language_from_text("नवीन पॅन कार्ड मिळवण्यासाठी काय करावे लागेल?")
    assert_eq("Detect Marathi query (with ळ and Marathi words)", r["detected_language"], "mr")

    # Marathi without ळ but Marathi markers
    r = detect_language_from_text("मला नवीन रेशन कार्ड पाहिजे माहिती सांगा")
    assert_eq("Detect Marathi query (lexical markers)", r["detected_language"], "mr")

    # Bengali
    r = detect_language_from_text("নতুন রেশন কার্ড কীভাবে বানাব?")
    assert_eq("Detect Bengali query", r["detected_language"], "bn")

    print("\n" + "=" * 60)
    print("2. INDEPENDENT UI LANGUAGE OVERRIDE TESTS")
    print("=" * 60)

    # Client is in Tamil, but user typed English
    lang = _detect_language_server_side("How to apply for driving license?", client_lang="ta")
    assert_eq("English query when UI is Tamil", lang, "en")

    # Client is in English, but user typed Tamil
    lang = _detect_language_server_side("பான் கார்டு விண்ணப்பிப்பது எப்படி?", client_lang="en")
    assert_eq("Tamil query when UI is English", lang, "ta")

    # Client is in English, but user typed Hindi
    lang = _detect_language_server_side("आधार कार्ड में नाम कैसे बदलें?", client_lang="en")
    assert_eq("Hindi query when UI is English", lang, "hi")

    # Client is in English, but user typed Marathi
    lang = _detect_language_server_side("नवीन ड्रायव्हिंग लायसन्स कसे काढायचे?", client_lang="en")
    assert_eq("Marathi query when UI is English", lang, "mr")

    # Client is in English, but user typed Bengali
    lang = _detect_language_server_side("পাসপোর্ট কীভাবে পাব?", client_lang="en")
    assert_eq("Bengali query when UI is English", lang, "bn")

    print("\n" + "=" * 60)
    print("3. TOPIC SWITCHING & CONTEXT RESOLUTION (THE CORE BUG)")
    print("=" * 60)

    # Simulate session with prior topic = Passport
    sid, sess = _get_or_create_session(None)
    sess["last_topic_id"] = "service_passport"
    sess["last_topic_name"] = "Passport Application & Renewal (Tatkaal / Normal)"
    sess["last_topic_type"] = "service"
    _push_history(sess, "How to apply for passport?", "Here are the passport details...")

    # Now user asks PAN in Tamil: "பான் கார்டு எப்படி விண்ணப்பிப்பது?"
    tamil_pan_query = "பான் கார்டு எப்படி விண்ணப்பிப்பது?"
    resolved = _resolve_query_with_context(tamil_pan_query, sess)
    assert_eq("Context resolution does NOT prepend Passport to Tamil PAN", resolved, tamil_pan_query)

    # Execute RAG on Tamil PAN
    rag_res = rag_service.answer_query(tamil_pan_query, lang="ta")
    assert_eq("Tamil PAN retrieval matches PAN Card, NOT Passport", rag_res.get("scheme_id"), "pan_card")
    assert_eq("Tamil PAN retrieval matched successfully", rag_res["matched"], True)

    # Now user asks complaint in English
    complaint_query = "How to lodge a complaint about delayed government service?"
    resolved_comp = _resolve_query_with_context(complaint_query, sess)
    assert_eq("Context resolution does NOT prepend Passport to complaint", resolved_comp, complaint_query)
    comp_res = rag_service.answer_query(complaint_query, lang="en")
    assert_eq("Complaint query matches Public Grievance, NOT Passport", comp_res.get("scheme_id"), "public_grievances")

    # Now simulate a GENUINE follow-up question
    # "What documents are required for this?"
    followup_q = "What documents are required for this?"
    resolved_followup = _resolve_query_with_context(followup_q, sess)
    expected_followup = f"{sess['last_topic_name']} {followup_q}"
    assert_eq("Genuine follow-up correctly enriched with prior topic", resolved_followup, expected_followup)

    print("\n" + "=" * 60)
    print("4. ALL 13 SERVICES COVERAGE IN MULTIPLE LANGUAGES")
    print("=" * 60)

    services_to_test = [
        ("passport", "How do I apply for a passport?", "en", "passport"),
        ("pan_card", "பான் கார்டு பெற என்ன செய்ய வேண்டும்?", "ta", "pan_card"),
        ("aadhaar", "नया आधार कार्ड कैसे बनवाएं?", "hi", "aadhaar"),
        ("driving_licence", "नवीन ड्रायव्हिंग लायसन्स कसे काढायचे?", "mr", "driving_licence"),
        ("voter_id", "নতুন ভোটার কার্ডের জন্য কীভাবে আবেদন করব?", "bn", "voter_id"),
        ("birth_certificate", "How to get a birth certificate?", "en", "birth_certificate"),
        ("death_certificate", "இறப்புச் சான்றிதழ் பெறுவது எப்படி?", "ta", "death_certificate"),
        ("income_caste_cert", "आय और जाति प्रमाण पत्र कैसे प्राप्त करें?", "hi", "income_caste_certificate"),
        ("ration_card", "नवीन रेशन कार्डसाठी अर्ज कसा करावा?", "mr", "ration_card"),
        ("scholarships", "সরকারি স্কলারশিপ কীভাবে পাব?", "bn", "scholarship_portal"),
        ("public_grievance", "How to register a grievance on CPGRAMS?", "en", "public_grievances"),
        ("record_correction", "பெயர் மற்றும் பிறந்த தேதி திருத்தம் செய்வது எப்படி?", "ta", "record_corrections"),
        ("ayushman_pmjay", "आयुष्मान भारत कार्ड कैसे बनवाएं?", "hi", "ayushman_bharat_pmjay"),
    ]

    for label, query, lang, expected_type in services_to_test:
        res = rag_service.answer_query(query, lang=lang)
        assert_eq(f"Service '{label}' in {lang}", res.get("scheme_id"), expected_type)
        if not res.get("matched"):
            print(f"  [WARN] {label} was not matched!")

    print("\n" + "=" * 60)
    print("5. UNRELATED QUERY HANDLING (NO HALLUCINATION)")
    print("=" * 60)

    unrelated_queries = [
        "How to make vegetable biryani?",
        "What is the weather in Delhi?",
        "Who won the cricket match yesterday?"
    ]
    for uq in unrelated_queries:
        res = rag_service.answer_query(uq, lang="en")
        assert_eq(f"Unrelated query '{uq}' matched flag", res["matched"], False)
        # Verify it does not bind to any scheme or service
        assert_eq(f"Unrelated query '{uq}' has scheme_id None", res.get("scheme_id"), None)

    print("\n" + "=" * 60)
    print("6. SCHEME MATCHING IN ALL LANGUAGES")
    print("=" * 60)

    for l in ["ta", "en", "hi", "mr", "bn"]:
        profile = {"age": 65, "gender": "female", "annual_income": 20000, "occupation": "homemaker"}
        matches = match_schemes(profile, lang=l)
        top = matches[0]
        assert_eq(f"Scheme match lang={l} has scheme_name", bool(top["scheme_name"]), True)
        assert_eq(f"Scheme match lang={l} has benefit", bool(top["benefit"]), True)
        assert_eq(f"Scheme match lang={l} has disclaimer", bool(top["disclaimer"]), True)

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} / {total} tests PASSED ({passed*100//total}%)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
