import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.ocr_service import check_document_readiness, SAMPLE_DOCUMENTS

def test_sample_valid_oap_high_score():
    result = check_document_readiness(
        sample_id="sample_valid_oap",
        scheme_id="old_age_pension",
        lang="en"
    )
    assert result["readiness_score"] >= 75, f"Expected score >= 75, got {result['readiness_score']}"
    assert result["is_ready"] is True
    assert len(result["identified_items"]) >= 3
    assert "Aadhaar" in str(result["identified_items"])
    assert "Age" in str(result["identified_items"]) or "65" in str(result["identified_items"])
    print("[PASS] test_sample_valid_oap_high_score")

def test_sample_incomplete_low_score():
    result = check_document_readiness(
        sample_id="sample_incomplete",
        scheme_id="old_age_pension",
        lang="ta"
    )
    assert result["readiness_score"] < 75, f"Expected score < 75, got {result['readiness_score']}"
    assert result["is_ready"] is False
    assert len(result["missing_items"]) >= 2
    print("[PASS] test_sample_incomplete_low_score")

def test_sample_pm_kisan_land_record():
    result = check_document_readiness(
        sample_id="sample_pm_kisan",
        scheme_id="pm_kisan",
        lang="ta"
    )
    assert result["readiness_score"] >= 75
    assert result["is_ready"] is True
    assert any("பட்டா" in item or "நில" in item for item in result["identified_items"])
    print("[PASS] test_sample_pm_kisan_land_record")

def test_tamil_voice_summary_generated():
    result = check_document_readiness(
        sample_id="sample_valid_oap",
        scheme_id="old_age_pension",
        lang="ta"
    )
    assert "உங்கள் ஆவணப் பரிசோதனை முடிந்தது" in result["voice_summary"]
    assert "இ-சேவை" in result["voice_summary"]
    print("[PASS] test_tamil_voice_summary_generated")

if __name__ == "__main__":
    test_sample_valid_oap_high_score()
    test_sample_incomplete_low_score()
    test_sample_pm_kisan_land_record()
    test_tamil_voice_summary_generated()
    print("ALL BACKEND OCR TESTS PASSED SUCCESSFULLY!")
