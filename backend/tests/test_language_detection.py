import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.language_detection_service import detect_language_from_text

def test_tamil_detection():
    # Tamil script query about pension
    res = detect_language_from_text("முதியோர் ஓய்வூதியத் திட்டம் பற்றி சொல்லுங்கள்")
    assert res["detected_language"] == "ta"
    assert res["native_name"] == "தமிழ்"
    assert res["confidence"] >= 0.8
    print("[PASS] test_tamil_detection")

def test_hindi_detection():
    # Hindi Devanagari query about kisan yojana
    res = detect_language_from_text("मुझे किसान सम्मान निधि योजना के बारे में जानकारी चाहिए")
    assert res["detected_language"] == "hi"
    assert res["native_name"] == "हिन्दी"
    assert res["confidence"] >= 0.8
    print("[PASS] test_hindi_detection")

def test_marathi_detection():
    # Marathi Devanagari query about shetkari yojana
    res = detect_language_from_text("शेतकरी योजना कशी मिळेल मला माहिती पाहिजे")
    assert res["detected_language"] == "mr"
    assert res["native_name"] == "मराठी"
    assert res["confidence"] >= 0.8
    print("[PASS] test_marathi_detection")

def test_bengali_detection():
    # Bengali script query about pension
    res = detect_language_from_text("বৃদ্ধ পেনশন যোজনা সম্পর্কে জানতে চাই")
    assert res["detected_language"] == "bn"
    assert res["native_name"] == "বাংলা"
    assert res["confidence"] >= 0.8
    print("[PASS] test_bengali_detection")

def test_english_detection():
    # English query about PM kisan
    res = detect_language_from_text("How can I apply for the farmer PM Kisan scheme?")
    assert res["detected_language"] == "en"
    assert res["native_name"] == "English"
    assert res["confidence"] >= 0.7
    print("[PASS] test_english_detection")

if __name__ == "__main__":
    test_tamil_detection()
    test_hindi_detection()
    test_marathi_detection()
    test_bengali_detection()
    test_english_detection()
    print("ALL LANGUAGE DETECTION TESTS PASSED SUCCESSFULLY!")
