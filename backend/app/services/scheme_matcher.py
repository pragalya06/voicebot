"""
Scheme Matching Engine: Evaluates citizen profile attributes against
official scheme requirements and produces transparent match justifications.
"""

from typing import List, Dict, Any
from app.data.schemes_data import VERIFIED_SCHEMES

class CitizenProfile:
    def __init__(self, data: dict):
        self.age = int(data.get("age", 30))
        self.gender = data.get("gender", "female") # "female", "male", "other"
        self.occupation = data.get("occupation", "homemaker") # "farmer", "laborer", "homemaker", "salaried", "business"
        self.annual_income = int(data.get("annual_income", 50000))
        self.is_rural = data.get("is_rural", True)
        self.has_cultivable_land = data.get("has_cultivable_land", False)
        self.marital_status = data.get("marital_status", "married") # "married", "single", "widow", "destitute"
        self.electricity_units_yearly = int(data.get("electricity_units_yearly", 2000))

def match_schemes(profile_data: dict, lang: str = "ta") -> List[Dict[str, Any]]:
    profile = CitizenProfile(profile_data)
    is_tamil = (lang == "ta")
    results = []

    for s in VERIFIED_SCHEMES:
        scheme_id = s["id"]
        reasons_en = []
        reasons_ta = []
        missing_en = []
        missing_ta = []
        match_score = 0
        is_eligible = False

        # --- 1. Old Age Pension (OAP) ---
        if scheme_id == "old_age_pension":
            if profile.age >= 60:
                match_score += 50
                reasons_en.append(f"Age is {profile.age} (meets 60+ age threshold).")
                reasons_ta.append(f"உங்கள் வயது {profile.age} (60 வயது வரம்பை பூர்த்தி செய்கிறது).")
                
                if profile.annual_income <= 24000:
                    match_score += 40
                    reasons_en.append("Annual income is within the ₹24,000 BPL threshold.")
                    reasons_ta.append("ஆண்டு வருமானம் ₹24,000-க்குள் உள்ளது.")
                    is_eligible = True
                else:
                    missing_en.append("Annual income reported exceeds standard ₹24,000 rural pension limit; official BPL verification required.")
                    missing_ta.append("வருமானம் ₹24,000-க்கு மேல் உள்ளது; வட்டாட்சியர் கள ஆய்வு மற்றும் வறுமைக்கோட்டுச் சான்று தேவை.")
                    match_score += 20
                
                missing_en.append("Requires proof of no earning adult children capable of supporting applicant.")
                missing_ta.append("ஆதரவற்றவர் மற்றும் குடும்ப உதவி இல்லை என்பதற்கான சான்று தேவை.")
            else:
                missing_en.append(f"Current age is {profile.age}; minimum requirement is 60 years.")
                missing_ta.append(f"தற்போதைய வயது {profile.age}; குறைந்தபட்சம் 60 வயது பூர்த்தியாகியிருக்க வேண்டும்.")

        # --- 2. Kalaignar Magalir Urimai Thogai ---
        elif scheme_id == "kalaignar_magalir_urimai":
            if profile.gender == "female" and profile.age >= 21:
                match_score += 45
                reasons_en.append("Female family head aged 21 or older.")
                reasons_ta.append("21 வயதுக்கு மேற்பட்ட பெண் குடும்பத் தலைவர்.")

                if profile.annual_income <= 250000:
                    match_score += 40
                    reasons_en.append(f"Annual income (₹{profile.annual_income:,}) is below the ₹2.5 Lakh ceiling.")
                    reasons_ta.append(f"குடும்ப ஆண்டு வருமானம் (₹{profile.annual_income:,}) ₹2.5 லட்சத்திற்குள் உள்ளது.")
                    is_eligible = True
                else:
                    missing_en.append("Annual income exceeds ₹2.5 Lakh limit.")
                    missing_ta.append("குடும்ப ஆண்டு வருமானம் ₹2.5 லட்சத்திற்கு மேல் உள்ளது.")

                if profile.electricity_units_yearly <= 3600:
                    reasons_en.append("Domestic electricity consumption is within 3,600 units limit.")
                    reasons_ta.append("மின்சார பயன்பாடு ஆண்டுக்கு 3,600 யூனிட்டுகளுக்குள் உள்ளது.")
                else:
                    missing_en.append("Domestic electricity usage exceeds 3,600 units/year.")
                    missing_ta.append("வீட்டு மின் நுகர்வு ஆண்டுக்கு 3,600 யூனிட்டுக்கு மேல் உள்ளது.")

                missing_en.append("Subject to landholding ceiling (< 5 acres wetland or < 10 acres dryland).")
                missing_ta.append("நில வரம்பு (5 ஏக்கர் நஞ்சை / 10 ஏக்கர் புஞ்சை) சரிபார்ப்புக்கு உட்பட்டது.")
            else:
                if profile.gender != "female":
                    missing_en.append("Scheme is reserved for female heads of family.")
                    missing_ta.append("இத்திட்டம் குடும்பத்தின் பெண் தலைவருக்கு மட்டுமே உரியது.")
                if profile.age < 21:
                    missing_en.append(f"Age {profile.age} is below minimum 21 years requirement.")
                    missing_ta.append(f"வயது {profile.age}; குறைந்தபட்சம் 21 வயது இருக்க வேண்டும்.")

        # --- 3. PM-KISAN ---
        elif scheme_id == "pm_kisan":
            if profile.occupation == "farmer" or profile.has_cultivable_land:
                match_score += 55
                reasons_en.append("Occupation is agriculture / cultivable landholding declared.")
                reasons_ta.append("விவசாயத் தொழில் / சாகுபடி நில உரிமை குறிப்பிடப்பட்டுள்ளது.")

                if profile.annual_income <= 300000:
                    match_score += 35
                    is_eligible = True
                    reasons_en.append("Income profile qualifies under small/marginal farmer parameters.")
                    reasons_ta.append("சிறு மற்றும் குறு விவசாயி வரம்பிற்குள் உள்ளது.")

                missing_en.append("Requires valid land ownership record (Patta/Chitta) and Aadhaar e-KYC.")
                missing_ta.append("விவசாயியின் பெயரில் உள்ள பட்டா/சிட்டா மற்றும் ஆதார் e-KYC சரிபார்ப்பு தேவை.")
            else:
                missing_en.append("Applicable only for families owning agricultural cultivable land in their name.")
                missing_ta.append("சொந்த பெயரில் சாகுபடி விவசாய நிலம் உள்ள குடும்பங்களுக்கு மட்டுமே பொருந்தும்.")

        # --- 4. CMCHIS Health Insurance ---
        elif scheme_id == "cmchis_health":
            if profile.annual_income <= 120000:
                match_score += 85
                is_eligible = True
                reasons_en.append(f"Family income (₹{profile.annual_income:,}) qualifies within ₹1.2 Lakh threshold.")
                reasons_ta.append(f"குடும்ப ஆண்டு வருமானம் (₹{profile.annual_income:,}) ₹1.20 லட்சத்திற்குள் உள்ளது.")
                missing_en.append("Smart Ration Card and VAO income certificate required at District Kiosk.")
                missing_ta.append("ஸ்மார்ட் குடும்ப அட்டை மற்றும் கிராம நிர்வாக அலுவலர் வருமானச் சான்று தேவை.")
            else:
                match_score += 20
                missing_en.append("Family annual income exceeds ₹1.2 Lakh eligibility ceiling.")
                missing_ta.append("குடும்ப ஆண்டு வருமானம் ₹1.20 லட்சத்திற்கு மேல் உள்ளது.")

        # --- 5. Destitute Widow Pension (DWP) ---
        elif scheme_id == "widow_destitute_pension":
            if profile.marital_status == "widow" and profile.age >= 18:
                match_score += 60
                reasons_en.append("Widowed female aged 18+.")
                reasons_ta.append("18 வயதுக்கு மேற்பட்ட விதவை பெண்.")

                if profile.annual_income <= 24000:
                    match_score += 30
                    is_eligible = True
                    reasons_en.append("Annual income within destitute pension criteria (≤ ₹24,000).")
                    reasons_ta.append("ஆண்டு வருமானம் ஆதரவற்றோர் ஓய்வூதிய வரம்பிற்குள் (≤ ₹24,000) உள்ளது.")
                else:
                    missing_en.append("Income reported above standard destitute threshold; Tahsildar discretion applies.")
                    missing_ta.append("வருமானம் வரம்பை விட கூடுதலாக உள்ளது; வட்டாட்சியர் ஆய்வு தேவை.")

                missing_en.append("Husband's death certificate and Destitute Widow Certificate required.")
                missing_ta.append("கணவரின் இறப்புச் சான்றிதழ் மற்றும் வட்டாட்சியர் விதவைச் சான்று தேவை.")
            else:
                missing_en.append("Applicable specifically to destitute widowed women aged 18 and older.")
                missing_ta.append("18 வயதுக்கு மேற்பட்ட ஆதரவற்ற விதவை பெண்களுக்கு மட்டுமே பொருந்தும்.")

        # Normalize score
        match_score = min(match_score, 100)

        # Build recommendation card payload
        status_label = "HIGH" if match_score >= 70 else ("MODERATE" if match_score >= 40 else "LOW")
        
        results.append({
            "scheme_id": scheme_id,
            "scheme_name": s["name_ta"] if is_tamil else s["name_en"],
            "category": s["category"],
            "benefit": s["benefit_ta"] if is_tamil else s["benefit_en"],
            "match_score": match_score,
            "status": status_label,
            "is_eligible": is_eligible,
            "why_matched": reasons_ta if is_tamil else reasons_en,
            "missing_info": missing_ta if is_tamil else missing_en,
            "required_documents": s["required_documents_ta"] if is_tamil else s["required_documents_en"],
            "official_portal": s["official_portal"],
            "disclaimer": (
                "இது முதற்கட்ட மதிப்பீடு மட்டுமே. அரசு அலுவலகத்தில் சான்றிதழ்கள் சரிபார்க்கப்பட்ட பிறகே இறுதி தகுதி தீர்மானிக்கப்படும்."
                if is_tamil else
                "This is an advisory assessment. Official eligibility is determined solely after document verification by authorities."
            )
        })

    # Sort so top recommendations appear first
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
