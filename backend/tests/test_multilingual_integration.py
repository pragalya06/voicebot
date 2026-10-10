import os
import sys

# Ensure UTF-8 output on Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.language_detection_service import detect_language_from_text
from app.services.rag_service import rag_service

def test_multilingual_assistant_pipeline():
    test_cases = [
        {
            "query": "முதியோர் ஓய்வூதியத் திட்டம் பற்றி சொல்லுங்கள்",
            "expected_lang": "ta",
            "expected_keyword": "ஓய்வூதிய"
        },
        {
            "query": "मुझे किसान सम्मान निधि योजना की जानकारी चाहिए",
            "expected_lang": "hi",
            "expected_keyword": "योजना"
        },
        {
            "query": "शेतकरी योजना कशी मिळेल मला माहिती पाहिजे",
            "expected_lang": "mr",
            "expected_keyword": "योजना"
        },
        {
            "query": "বৃদ্ধ পেনশন যোজনা সম্পর্কে জানতে চাই",
            "expected_lang": "bn",
            "expected_keyword": "প্রকল্প"
        },
        {
            "query": "How can I apply for the farmer PM Kisan scheme?",
            "expected_lang": "en",
            "expected_keyword": "Scheme"
        }
    ]

    for tc in test_cases:
        # 1. Test Language Detection
        lid = detect_language_from_text(tc["query"])
        assert lid["detected_language"] == tc["expected_lang"], f"Expected {tc['expected_lang']}, got {lid['detected_language']}"

        # 2. Test RAG Assistant Response in that language
        ans = rag_service.answer_query(tc["query"], lang=lid["detected_language"])
        assert ans["matched"] is True, f"Failed match for query: {tc['query']}"
        assert tc["expected_keyword"] in ans["answer"], f"Expected '{tc['expected_keyword']}' in answer for {tc['expected_lang']}"
        assert len(ans["voice_summary"]) > 10, f"Voice summary too short for {tc['expected_lang']}"
        print(f"[PASS] Multilingual pipeline test for: {lid['language_name']} ({lid['detected_language']})")

if __name__ == "__main__":
    test_multilingual_assistant_pipeline()
    print("ALL 5 LANGUAGES (TAMIL, HINDI, MARATHI, BENGALI, ENGLISH) PASSED SUCCESSFULLY!")
