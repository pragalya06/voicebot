"""
Manual verification tests for the key fixes.
Run: .\\venv\\Scripts\\python.exe tests\\verify_fixes.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.language_detection_service import detect_language_from_text
from app.api.routes_assistant import _resolve_query_with_context, _detect_language_server_side

PASS = "✅ PASS"
FAIL = "❌ FAIL"

def check(label, condition):
    print(f"  {PASS if condition else FAIL}  {label}")
    return condition

results = []

print("\n═══════════════════════════════════════════")
print("  SevaMitra Fix Verification Tests")
print("═══════════════════════════════════════════\n")

# ─── 1. Language Detection ─────────────────────────────────────────────────
print("1. Language Detection (all 5 languages)")

tests = [
    ("English", "How do I apply for a passport?", "en"),
    ("Tamil (native)", "முதியோர் ஓய்வூதியத் திட்டம் பற்றி சொல்லுங்கள்", "ta"),
    ("Hindi (native)", "पासपोर्ट के लिए आवेदन कैसे करें", "hi"),
    ("Marathi (native)", "शेतकरी योजना कशी मिळेल मला माहिती पाहिजे", "mr"),
    ("Bengali (native)", "পাসপোর্ট আবেদন কিভাবে করবো", "bn"),
]

for label, text, expected_lang in tests:
    result = detect_language_from_text(text)
    ok = result["detected_language"] == expected_lang
    results.append(ok)
    check(f"{label}: '{text[:40]}' → {result['detected_language']} (expected {expected_lang}, conf={result['confidence']:.2f})", ok)

# ─── 2. Hindi vs Marathi disambiguation ───────────────────────────────────
print("\n2. Hindi / Marathi disambiguation (same Devanagari script)")
hindi_only = "पासपोर्ट के लिए आवेदन कैसे करें"
marathi_only = "शेतकरी योजना कशी मिळेल मला माहिती पाहिजे"

hi_res = detect_language_from_text(hindi_only)
mr_res = detect_language_from_text(marathi_only)

ok_hi = hi_res["detected_language"] == "hi"
ok_mr = mr_res["detected_language"] == "mr"
results += [ok_hi, ok_mr]
check(f"Hindi detected as hi (not mr): {hi_res['detected_language']}", ok_hi)
check(f"Marathi detected as mr (not hi): {mr_res['detected_language']}", ok_mr)

# ─── 3. Server-side language detection override ────────────────────────────
print("\n3. Server-side language override (non-Latin scripts override client hint)")
# Backend should override wrong client hint for native-script queries
for text, client_hint, expected in [
    ("முதியோர் ஓய்வூதியம்", "en", "ta"),       # Tamil script → override en
    ("পাসপোর্ট আবেদন", "hi", "bn"),            # Bengali script → override hi
    ("how to apply for passport", "ta", "en"),  # English text, client says ta → keep en
]:
    detected = _detect_language_server_side(text, client_hint)
    ok = detected == expected
    results.append(ok)
    check(f"text='{text[:30]}' client='{client_hint}' → '{detected}' (expected '{expected}')", ok)

# ─── 4. Follow-up vs new topic resolution ─────────────────────────────────
print("\n4. Follow-up / topic-change detection")

dummy_session_passport = {
    "last_topic_id": "passport",
    "last_topic_name": "Passport",
    "last_topic_type": "service",
    "history": [],
}

dummy_session_none = {
    "last_topic_id": None,
    "last_topic_name": None,
    "last_topic_type": None,
    "history": [],
}

followup_cases = [
    ("What documents do I need?",    dummy_session_passport, True,  "short follow-up → enriched"),
    ("What is the fee?",             dummy_session_passport, True,  "fee follow-up → enriched"),
    ("How do I apply for Aadhaar?",  dummy_session_passport, False, "new topic Aadhaar → not enriched"),
    ("Tell me about PAN card",       dummy_session_passport, False, "new topic PAN → not enriched"),
    ("How to apply for passport",    dummy_session_none,     False, "no prior context → not enriched"),
]

for query, sess, should_enrich, label in followup_cases:
    resolved = _resolve_query_with_context(query, sess)
    was_enriched = resolved != query
    ok = was_enriched == should_enrich
    results.append(ok)
    check(f"{label}: '{query[:40]}' → {'enriched' if was_enriched else 'unchanged'}", ok)

# ─── 5. Substring false-positive guard ────────────────────────────────────
print("\n5. Substring false-positive guard (new-topic words embedded in longer text)")
# "information about pension" should NOT match "for" as a follow-up signal
tricky = "I need more information about the passport application process"
resolved_tricky = _resolve_query_with_context(tricky, dummy_session_passport)
# "passport" is a NEW_TOPIC_SIGNAL → should NOT enrich
ok_tricky = resolved_tricky == tricky
results.append(ok_tricky)
check(f"'...passport application process' not enriched (passport is new-topic signal): {ok_tricky}", ok_tricky)

# ─── Summary ──────────────────────────────────────────────────────────────
total = len(results)
passed = sum(results)
print(f"\n═══════════════════════════════════════════")
print(f"  Results: {passed}/{total} passed")
print(f"═══════════════════════════════════════════\n")
if passed < total:
    sys.exit(1)
