import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.api.routes_checklist import SCHEME_ROADMAPS, TRACKING_DEMOS

def test_roadmaps_catalog():
    assert "old_age_pension" in SCHEME_ROADMAPS
    assert "kalaignar_magalir_urimai" in SCHEME_ROADMAPS
    assert "pm_kisan" in SCHEME_ROADMAPS

    oap = SCHEME_ROADMAPS["old_age_pension"]
    assert len(oap["steps"]) == 5
    assert "VAO" in oap["steps"][0]["title_en"]
    assert "கிராம நிர்வாக அலுவலரிடம்" in oap["steps"][0]["title_ta"]
    print("[PASS] test_roadmaps_catalog")

def test_tracking_demos():
    assert "TN-OAP-2026-8941029" in TRACKING_DEMOS
    demo = TRACKING_DEMOS["TN-OAP-2026-8941029"]
    assert demo["current_status"] == "approved"
    assert len(demo["stages"]) == 4
    assert demo["stages"][0]["status"] == "completed"
    print("[PASS] test_tracking_demos")

if __name__ == "__main__":
    test_roadmaps_catalog()
    test_tracking_demos()
    print("ALL BACKEND GUIDANCE & TRACKING TESTS PASSED SUCCESSFULLY!")
