from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

router = APIRouter(prefix="/api/guidance", tags=["Application Guidance & Tracking"])

# Step & Roadmap Models
class GuidanceStep(BaseModel):
    step_number: int
    title_en: str
    title_ta: str
    description_en: str
    description_ta: str
    authority_en: str
    authority_ta: str
    estimated_days: str
    pitfalls_en: Optional[str] = None
    pitfalls_ta: Optional[str] = None

class SchemeRoadmap(BaseModel):
    scheme_id: str
    scheme_name_en: str
    scheme_name_ta: str
    required_documents_en: List[str]
    required_documents_ta: List[str]
    steps: List[GuidanceStep]
    voice_summary_en: str
    voice_summary_ta: str

# Tracking Status Models
class TrackingStage(BaseModel):
    stage_number: int
    title_en: str
    title_ta: str
    status: str  # 'completed', 'current', 'pending', 'alert'
    date: str
    officer_note_en: str
    officer_note_ta: str

class ApplicationStatusResponse(BaseModel):
    reference_number: str
    scheme_id: str
    scheme_name_en: str
    scheme_name_ta: str
    applicant_name: str
    submission_date: str
    current_status: str  # 'approved', 'under_review', 'action_required'
    stages: List[TrackingStage]
    voice_summary_en: str
    voice_summary_ta: str
    disclaimer_en: str
    disclaimer_ta: str

# In-Memory Scheme Roadmaps Catalog
SCHEME_ROADMAPS: Dict[str, Dict[str, Any]] = {
    "old_age_pension": {
        "scheme_id": "old_age_pension",
        "scheme_name_en": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
        "scheme_name_ta": "முதியோர் ஓய்வூதியத் திட்டம் (OAP)",
        "required_documents_en": [
            "Aadhaar Card Copy",
            "Income & Age Certificate issued by Tahsildar (< ₹24,000/yr)",
            "Smart Ration Card (Rice Card)",
            "Aadhaar-seeded Bank Passbook front page",
            "Passport size photograph"
        ],
        "required_documents_ta": [
            "ஆதார் அட்டை நகல்",
            "வட்டாட்சியர் வழங்கிய வருமானச் சான்றிதழ் (ஆண்டுக்கு < ₹24,000)",
            "ஸ்மார்ட் குடும்ப அட்டை (அரிசி அட்டை)",
            "ஆதாருடன் இணைக்கப்பட்ட வங்கி கணக்கு புத்தக முதல் பக்கம்",
            "பாஸ்போர்ட் அளவு புகைப்படம்"
        ],
        "steps": [
            {
                "step_number": 1,
                "title_en": "Obtain Income & Age Certificate from VAO",
                "title_ta": "கிராம நிர்வாக அலுவலரிடம் (VAO) வருமானச் சான்று பெறுதல்",
                "description_en": "Meet your local Village Administrative Officer (VAO) to verify your age (60+) and family income.",
                "description_ta": "உங்கள் கிராம நிர்வாக அலுவலரை (VAO) சந்தித்து 60 வயது பூர்த்தி மற்றும் குடும்ப வருமானத்தை சரிபார்க்கவும்.",
                "authority_en": "Village Administrative Officer (VAO)",
                "authority_ta": "கிராம நிர்வாக அலுவலர் (VAO)",
                "estimated_days": "1 - 2 Days",
                "pitfalls_en": "Ensure family income is listed under ₹24,000/yr and no earning adult sons reside in the household.",
                "pitfalls_ta": "குடும்ப வருமானம் ₹24,000க்கு கீழ் உள்ளதா மற்றும் வருமானம் ஈட்டும் வயது வந்த மகன்கள் இல்லையா என்பதை உறுதிசெய்க."
            },
            {
                "step_number": 2,
                "title_en": "Submit Application at e-Seva / CSC Centre",
                "title_ta": "இ-சேவை மையத்தில் விண்ணப்பம் பதிவு செய்தல்",
                "description_en": "Visit your nearest e-Seva centre with Aadhaar, Income Certificate, and Ration card for biometric application entry.",
                "description_ta": "அருகிலுள்ள இ-சேவை மையத்திற்கு சென்று ஆதார், வருமானச் சான்று, ரேஷன் கார்டுடன் விண்ணப்பத்தை பதிவு செய்யவும்.",
                "authority_en": "e-Seva Centre / Common Service Centre",
                "authority_ta": "இ-சேவை மையம் / பொது சேவை மையம்",
                "estimated_days": "Same Day",
                "pitfalls_en": "Collect the printed acknowledgement slip containing your TN-OAP reference number.",
                "pitfalls_ta": "TN-OAP குறிப்பு எண் கொண்ட அச்சிடப்பட்ட ஒப்புதல் சீட்டை மறக்காமல் பெற்றுக்கொள்ளவும்."
            },
            {
                "step_number": 3,
                "title_en": "Field Verification by Revenue Inspector (RI)",
                "title_ta": "வருவாய் ஆய்வாளர் (RI) கள தணிக்கை",
                "description_en": "Revenue Inspector conducts field verification to ensure applicant is living independently without major income.",
                "description_ta": "வருவாய் ஆய்வாளர் நேரடி கள ஆய்வு செய்து விண்ணப்பதாரரின் வாழ்வாதாரத்தை சரிபார்ப்பார்.",
                "authority_en": "Revenue Inspector (RI / Taluk Office)",
                "authority_ta": "வருவாய் ஆய்வாளர் (RI / தாலுகா அலுவலகம்)",
                "estimated_days": "7 - 10 Days",
                "pitfalls_en": "Be present at your residential address with original documents during verification visit.",
                "pitfalls_ta": "ஆய்வின் போது அசல் ஆவணங்களுடன் வீட்டில் இருப்பதை உறுதிசெய்க."
            },
            {
                "step_number": 4,
                "title_en": "Tahsildar Sanction Approval",
                "title_ta": "வட்டாட்சியர் ஒப்புதல் & ஆணை பிறப்பித்தல்",
                "description_en": "Special Tahsildar Social Security Scheme (SSS) reviews the RI recommendation and issues official sanction order.",
                "description_ta": "சமூகப் பாதுகாப்புத் திட்ட தனி வட்டாட்சியர் பரிந்துரையை பரிசீலித்து ஓய்வூதிய ஆணையை பிறப்பிப்பார்.",
                "authority_en": "Special Tahsildar (Social Security Schemes)",
                "authority_ta": "தனி வட்டாட்சியர் (சமூகப் பாதுகாப்புத் திட்டம்)",
                "estimated_days": "15 - 20 Days",
                "pitfalls_en": "Track sanction status using your reference slip.",
                "pitfalls_ta": "ஒப்புதல் சீட்டில் உள்ள எண்ணைக் கொண்டு தாலுகா அலுவலகத்தில் நிலை அறியலாம்."
            },
            {
                "step_number": 5,
                "title_en": "Direct Monthly Credit (DBT) to Bank Account",
                "title_ta": "வங்கி கணக்கில் மாதந்தோறும் நேரிடி உதவித்தொகை வரவு",
                "description_en": "Monthly pension of ₹1,000 / ₹1,200 is directly credited to your Aadhaar-linked bank account via Direct Benefit Transfer.",
                "description_ta": "மாதாந்திர உதவித்தொகை ₹1,000 / ₹1,200 உங்கள் ஆதாருடன் இணைக்கப்பட்ட வங்கி கணக்கில் நேரடியாக வரவு வைக்கப்படும்.",
                "authority_en": "Treasury Department & Bank",
                "authority_ta": "கருவூலத் துறை மற்றும் வங்கி",
                "estimated_days": "Monthly on 1st - 5th",
                "pitfalls_en": "Keep bank account active and ensure NPCI Aadhaar seeding is completed.",
                "pitfalls_ta": "வங்கி கணக்கை பயன்பாட்டில் வைத்திருக்கவும்; ஆதாருடன் NPCI இணைப்பு உள்ளதை உறுதிசெய்க."
            }
        ],
        "voice_summary_en": "Applying for Old Age Pension has 5 steps: First, get an income proof from your VAO. Second, submit documents at the e-Seva centre. Third, attend the Revenue Inspector verification. Fourth, obtain Tahsildar sanction order. Fifth, receive monthly credit in your bank account.",
        "voice_summary_ta": "முதியோர் ஓய்வூதியத்திற்கு விண்ணப்பிக்க 5 படிகள் உள்ளன: 1. கிராம நிர்வாக அலுவலரிடம் சான்று பெறுதல், 2. இ-சேவை மையத்தில் விண்ணப்பித்தல், 3. வருவாய் ஆய்வாளர் நேரில் சரிபார்த்தல், 4. வட்டாட்சியர் ஒப்புதல் ஆணை பெறுதல், 5. வங்கி கணக்கில் மாதாந்திர பணம் வரவு செய்யப்படுதல்."
    },

    "kalaignar_magalir_urimai": {
        "scheme_id": "kalaignar_magalir_urimai",
        "scheme_name_en": "Kalaignar Magalir Urimai Thogai Scheme (KMUT)",
        "scheme_name_ta": "கலைஞர் மகளிர் உரிமைத் திட்டம் (KMUT)",
        "required_documents_en": [
            "Smart Ration Card (Priority Household / Rice Card)",
            "Aadhaar Card of Woman Head of Household",
            "Electricity Bill Consumer Number",
            "Aadhaar-linked Bank Passbook copy"
        ],
        "required_documents_ta": [
            "ஸ்மார்ட் குடும்ப அட்டை (முன்னுரிமை அரிசி அட்டை)",
            "குடும்ப பெண் தலைவரின் ஆதார் அட்டை",
            "மின்சார கட்டண நுகர்வோர் எண்",
            "ஆதாருடன் இணைக்கப்பட்ட வங்கி கணக்கு புத்தக நகல்"
        ],
        "steps": [
            {
                "step_number": 1,
                "title_en": "Verify Ration Card Details",
                "title_ta": "ரேஷன் கார்டு விவரங்களை சரிபார்த்தல்",
                "description_en": "Ensure the applicant is listed as the woman head of household on your Smart Ration Card.",
                "description_ta": "ஸ்மார்ட் குடும்ப அட்டையில் விண்ணப்பதாரர் பெண் குடும்பத் தலைவராக உள்ளதை உறுதிசெய்க.",
                "authority_en": "Fair Price Shop / Civil Supplies Dept",
                "authority_ta": "நியாய விலைக் கடை / நுகர்வோர் பாதுகாப்புத் துறை",
                "estimated_days": "1 Day",
                "pitfalls_en": "Only one woman head per ration card is eligible.",
                "pitfalls_ta": "ஒரு குடும்ப அட்டையில் ஒரு பெண் தலைவருக்கு மட்டுமே உரிமைத் தொகை வழங்கப்படும்."
            },
            {
                "step_number": 2,
                "title_en": "Special Camp Registration / e-Seva Application",
                "title_ta": "சிறப்பு முகாம் / இ-சேவை மைய பதிவு",
                "description_en": "Register your application at the local Magalir Urimai special camp or designated e-Seva centre.",
                "description_ta": "உள்ளூர் மகளிர் உரிமை சிறப்பு முகாமில் அல்லது இ-சேவை மையத்தில் படிவத்தை சமர்ப்பிக்கவும்.",
                "authority_en": "KMUT Special Camp Team / e-Seva",
                "authority_ta": "KMUT சிறப்பு முகாம் குழு / இ-சேவை மையம்",
                "estimated_days": "Same Day",
                "pitfalls_en": "Bring registered mobile number for OTP authentication.",
                "pitfalls_ta": "OTP சரிபார்ப்பிற்கு குடும்ப அட்டையுடன் இணைக்கப்பட்ட அலைபேசியை கொண்டு செல்லவும்."
            },
            {
                "step_number": 3,
                "title_en": "Field Verification of Electricity & Land Ceiling",
                "title_ta": "மின் பயன்பாடு மற்றும் நில அளவு களச் சரிபார்ப்பு",
                "description_en": "Automated cross-verification of electricity consumption (<3,600 units/yr) and landholding records (<5 acres).",
                "description_ta": "மின்சார பயன்பாடு (ஆண்டுக்கு <3600 யூனிட்) மற்றும் நில அளவு கணினி மூலம் சரிபார்க்கப்படும்.",
                "authority_en": "Revenue Department & TANGEDCO Data",
                "authority_ta": "வருவாய்த் துறை மற்றும் மின்சார வாரிய தரவு",
                "estimated_days": "10 - 14 Days",
                "pitfalls_en": "Car or four-wheeler ownership registered in applicant's family will disqualify.",
                "pitfalls_ta": "குடும்பத்தில் சொந்தமாக நான்கு சக்கர வாகனம் (கார்) இருந்தால் தகுதியின்மை ஏற்படும்."
            },
            {
                "step_number": 4,
                "title_en": "Monthly Credit of ₹1,000 via Aadhaar Pay",
                "title_ta": "மாதந்தோறும் ₹1,000 வங்கி கணக்கில் நேரடியாக வரவு",
                "description_en": "₹1,000 is directly transferred to the woman head's bank account on the 15th of every month.",
                "description_ta": "ஒவ்வொரு மாதமும் 15-ஆம் தேதி ₹1,000 உதவித்தொகை நேரடியாக வங்கி கணக்கில் வரவு வைக்கப்படும்.",
                "authority_en": "TNeGA & State Bank of India",
                "authority_ta": "தமிழ்நாடு மின்ஆளுமை முகமை & எஸ்பிஐ",
                "estimated_days": "Monthly on 15th",
                "pitfalls_en": "If payment fails, check SMS notification for appeal guidelines at e-Seva.",
                "pitfalls_ta": "பணம் வரவில்லையெனில் இ-சேவை மையம் மூலம் மேல்முறையீடு செய்யலாம்."
            }
        ],
        "voice_summary_en": "Kalaignar Magalir Urimai scheme guidance: Verify woman head status on your Smart Ration Card, register at e-Seva special camp, pass electricity and land data cross-check, and receive 1,000 rupees monthly on the 15th.",
        "voice_summary_ta": "மகளிர் உரிமைத் திட்ட வழிகாட்டுதல்: 1. ரேஷன் அட்டையில் குடும்பத் தலைவராக இருக்க வேண்டும், 2. சிறப்பு முகாம் அல்லது இ-சேவையில் விண்ணப்பிக்கவும், 3. மின்சார பயன்பாடு சரிபார்க்கப்படும், 4. மாதந்தோறும் 15-ஆம் தேதி ₹1,000 வரவு வைக்கப்படும்."
    },

    "pm_kisan": {
        "scheme_id": "pm_kisan",
        "scheme_name_en": "PM-KISAN Samman Nidhi Scheme",
        "scheme_name_ta": "பிரதம மந்திரி கிசான் சம்மான் நிதி (PM-KISAN)",
        "required_documents_en": [
            "Aadhaar Card",
            "Patta / Chitta Land Ownership Extract",
            "Aadhaar-seeded Bank Passbook",
            "e-KYC Verification"
        ],
        "required_documents_ta": [
            "ஆதார் அட்டை",
            "பட்டா / சிட்டா நில உரிமை நகல்",
            "ஆதாருடன் இணைக்கப்பட்ட வங்கி கணக்கு புத்தகம்",
            "இ-கேஒய்சி (e-KYC) சரிபார்ப்பு"
        ],
        "steps": [
            {
                "step_number": 1,
                "title_en": "Obtain Land Patta / Chitta Extract",
                "title_ta": "பட்டா / சிட்டா நில சான்று பெறுதல்",
                "description_en": "Download digital Patta/Chitta copy from eservices.tn.gov.in showing land ownership under your name.",
                "description_ta": "eservices.tn.gov.in தளத்திலிருந்து உங்கள் பெயரிலுள்ள டிஜிட்டல் பட்டா/சிட்டா நகலை பதிவிறக்கவும்.",
                "authority_en": "Revenue Dept (e-Services Portal)",
                "authority_ta": "வருவாய்த் துறை (இ-சேவை தளம்)",
                "estimated_days": "1 Day",
                "pitfalls_en": "Land must be registered under applicant's name on or before 01-Feb-2019.",
                "pitfalls_ta": "நிலம் 01-பிப்ரவரி-2019 அன்றோ அதற்கு முன்னரோ உங்கள் பெயரில் பதிவாகியிருக்க வேண்டும்."
            },
            {
                "step_number": 2,
                "title_en": "Online Portal Registration at pmkisan.gov.in",
                "title_ta": "pmkisan.gov.in தளத்தில் புதிய உழவர் பதிவு",
                "description_en": "Self-register on PM-KISAN portal or visit CSC with Aadhaar and Patta details.",
                "description_ta": "PM-KISAN தளத்தில் அல்லது பொது சேவை மையத்தில் (CSC) ஆதார் மற்றும் பட்டா விவரங்களை பதிவு செய்யவும்.",
                "authority_en": "CSC / PM-KISAN Farmer Portal",
                "authority_ta": "பொது சேவை மையம் / பிஎம் கிசான் தளம்",
                "estimated_days": "Same Day",
                "pitfalls_en": "Enter exact name matching your Aadhaar Card.",
                "pitfalls_ta": "ஆதார் அட்டையில் உள்ளவாறே துல்லியமாக பெயரை தட்டச்சு செய்ய வேண்டும்."
            },
            {
                "step_number": 3,
                "title_en": "e-KYC & Aadhaar Bank Seeding",
                "title_ta": "இ-கேஒய்சி மற்றும் ஆதாருடன் வங்கி கணக்கு இணைப்பு",
                "description_en": "Complete biometric / OTP e-KYC on PM-KISAN portal and link bank account to Aadhaar NPCI.",
                "description_ta": "PM-KISAN தளத்தில் OTP மூலம் இ-கேஒய்சி செய்து உங்கள் வங்கி கணக்கை ஆதாருடன் இணைக்கவும்.",
                "authority_en": "Post Office / Bank / PM-KISAN Portal",
                "authority_ta": "அஞ்சலகம் / வங்கி / பிஎம் கிசான் தளம்",
                "estimated_days": "2 - 3 Days",
                "pitfalls_en": "Without active e-KYC, installment payments will be held.",
                "pitfalls_ta": "இ-கேஒய்சி முடிக்காவிட்டால் தவணைத் தொகை கணக்கில் வரவு செய்யப்படாது."
            },
            {
                "step_number": 4,
                "title_en": "Receive ₹6,000 Annual Benefit in 3 Installments",
                "title_ta": "ஆண்டுக்கு ₹6,000 உதவித்தொகை 3 தவணைகளாக பெறுதல்",
                "description_en": "Receive ₹2,000 every 4 months directly into your bank account.",
                "description_ta": "ஒவ்வொரு 4 மாதங்களுக்கும் ₹2,000 வீதம் ஆண்டுக்கு ₹6,000 வங்கி கணக்கில் நேரடியாக வரவு செய்யப்படும்.",
                "authority_en": "Ministry of Agriculture & Farmers Welfare",
                "authority_ta": "மத்திய வேளாண்மை அமைச்சகம்",
                "estimated_days": "Every 4 Months",
                "pitfalls_en": "Institutional landholders and income tax payers are not eligible.",
                "pitfalls_ta": "வருமான வரி செலுத்துவோர் மற்றும் தொண்டு நிறுவன நில உரிமையாளர்கள் தகுதியற்றவர்."
            }
        ],
        "voice_summary_en": "PM-KISAN application steps: Get your digital Patta extract, register online at pmkisan.gov.in, complete e-KYC verification, and receive ₹6,000 annually in 3 installments.",
        "voice_summary_ta": "பிஎம்-கிசான் விண்ணப்பிக்கும் வழிகாட்டி: 1. நில பட்டா நகல் பெறவும், 2. pmkisan.gov.in தளத்தில் பதிவு செய்யவும், 3. இ-கேஒய்சி பூர்த்தி செய்யவும், 4. 4 மாதங்களுக்கு ஒருமுறை ₹2,000 பெறவும்."
    }
}

# Simulated Tracking Records Database for Demonstration
TRACKING_DEMOS: Dict[str, Dict[str, Any]] = {
    "TN-OAP-2026-8941029": {
        "reference_number": "TN-OAP-2026-8941029",
        "scheme_id": "old_age_pension",
        "scheme_name_en": "Indira Gandhi Old Age Pension Scheme (IGNOAPS)",
        "scheme_name_ta": "முதியோர் ஓய்வூதியத் திட்டம் (OAP)",
        "applicant_name": "Meenakshi S.",
        "submission_date": "10-Jan-2026",
        "current_status": "approved",
        "stages": [
            {
                "stage_number": 1,
                "title_en": "Application Submitted at e-Seva Centre",
                "title_ta": "இ-சேவை மையத்தில் விண்ணப்பம் பதிவு செய்யப்பட்டது",
                "status": "completed",
                "date": "10-Jan-2026",
                "officer_note_en": "Biometric data and documents submitted successfully. Token No: 89410.",
                "officer_note_ta": "ஆவணங்கள் மற்றும் கைரேகை பதிவு பெறப்பட்டது. டோக்கன் எண்: 89410."
            },
            {
                "stage_number": 2,
                "title_en": "VAO & RI Field Inspection",
                "title_ta": "கிராம நிர்வாக அலுவலர் & RI நேரில் ஆய்வு",
                "status": "completed",
                "date": "16-Jan-2026",
                "officer_note_en": "Residence and age verified. Applicant age: 65, Income < ₹24,000. Approved for sanction.",
                "officer_note_ta": "வயது 65 மற்றும் வருமானம் ₹24,000க்கு கீழ் உள்ளதாக நேரடியாக சரிபார்க்கப்பட்டது."
            },
            {
                "stage_number": 3,
                "title_en": "Tahsildar Sanction Approval",
                "title_ta": "வட்டாட்சியர் அனுமதி ஆணை பிறப்பிப்பு",
                "status": "completed",
                "date": "24-Jan-2026",
                "officer_note_en": "Special Tahsildar (SSS) issued pension sanction order No: TN-MDU-OAP-4019.",
                "officer_note_ta": "தனி வட்டாட்சியர் (SSS) ஓய்வூதிய ஆணை வழங்கினார்: TN-MDU-OAP-4019."
            },
            {
                "stage_number": 4,
                "title_en": "First Monthly Credit via DBT",
                "title_ta": "முதல் மாதாந்திர தொகை வங்கி கணக்கில் வரவு",
                "status": "completed",
                "date": "01-Feb-2026",
                "officer_note_en": "₹1,000 credited to Canara Bank A/C ending in 4619.",
                "officer_note_ta": "கனரா வங்கி கணக்கில் ₹1,000 வரவு வைக்கப்பட்டது."
            }
        ],
        "voice_summary_en": "Application status for reference TN-OAP-2026-8941029: Sanctioned and Approved! Your application passed field verification and Tahsildar sanction. Monthly pension of 1,000 rupees is active.",
        "voice_summary_ta": "விண்ணப்ப நிலை TN-OAP-2026-8941029: ஒப்புதல் அளிக்கப்பட்டது! வருவாய் ஆய்வாளர் மற்றும் வட்டாட்சியர் ஒப்புதல் வழங்கிவிட்டனர். மாதாந்திர உதவித்தொகை ₹1,000 வரவு செயலில் உள்ளது."
    },

    "TN-KMUT-2026-5510293": {
        "reference_number": "TN-KMUT-2026-5510293",
        "scheme_id": "kalaignar_magalir_urimai",
        "scheme_name_en": "Kalaignar Magalir Urimai Thogai Scheme",
        "scheme_name_ta": "கலைஞர் மகளிர் உரிமைத் திட்டம்",
        "applicant_name": "Lakshmi R.",
        "submission_date": "22-Jan-2026",
        "current_status": "under_review",
        "stages": [
            {
                "stage_number": 1,
                "title_en": "Special Camp Application Registered",
                "title_ta": "சிறப்பு முகாமில் விண்ணப்பம் பதிவு செய்யப்பட்டது",
                "status": "completed",
                "date": "22-Jan-2026",
                "officer_note_en": "Ration Card and Aadhaar verified at ward special camp.",
                "officer_note_ta": "ரேஷன் கார்டு மற்றும் ஆதார் சரிபார்க்கப்பட்டு பதிவு செய்யப்பட்டது."
            },
            {
                "stage_number": 2,
                "title_en": "Electricity & Land Data Cross-Check",
                "title_ta": "மின் பயன்பாடு & நில தரவு கணினி சோதனை",
                "status": "current",
                "date": "28-Jan-2026",
                "officer_note_en": "TANGEDCO electricity usage cross-check in progress. Average units: 160 units/month.",
                "officer_note_ta": "மின்சார வாரிய நுகர்வோர் கணக்கு சரிபார்ப்பு நடைபெறுகிறது."
            },
            {
                "stage_number": 3,
                "title_en": "Final Selection List Inclusion",
                "title_ta": "இறுதி பயனாளிகள் பட்டியலில் சேர்த்தல்",
                "status": "pending",
                "date": "Pending",
                "officer_note_en": "Awaiting final approval for next monthly installment.",
                "officer_note_ta": "அடுத்த தவணைக்கான இறுதி ஒப்புதலுக்கு நிலுவையில் உள்ளது."
            },
            {
                "stage_number": 4,
                "title_en": "Monthly Credit of ₹1,000",
                "title_ta": "மாதாந்திர ₹1,000 வங்கி கணக்கில் வரவு",
                "status": "pending",
                "date": "Pending",
                "officer_note_en": "Scheduled upon approval.",
                "officer_note_ta": "ஒப்புதலுக்குப் பின் வங்கி கணக்கில் வரவு செய்யப்படும்."
            }
        ],
        "voice_summary_en": "Application status for reference TN-KMUT-2026-5510293: Currently under review. Step 2 electricity cross-check is in progress.",
        "voice_summary_ta": "விண்ணப்ப நிலை TN-KMUT-2026-5510293: பரிசீலனையில் உள்ளது. படி 2 மின் பயன்பாடு மற்றும் தரவு ஆய்வு நடைபெற்று வருகிறது."
    }
}

@router.get("/schemes", response_model=List[SchemeRoadmap])
async def list_all_roadmaps():
    """Returns step-by-step guidance roadmaps for all available government schemes."""
    return [SchemeRoadmap(**roadmap) for roadmap in SCHEME_ROADMAPS.values()]

@router.get("/schemes/{scheme_id}", response_model=SchemeRoadmap)
async def get_scheme_roadmap(scheme_id: str):
    """Returns detailed step-by-step guidance roadmap for a specific scheme."""
    if scheme_id not in SCHEME_ROADMAPS:
        scheme_id = "old_age_pension"
    return SchemeRoadmap(**SCHEME_ROADMAPS[scheme_id])

@router.get("/tracker/status", response_model=ApplicationStatusResponse)
async def track_application_status(ref_number: Optional[str] = Query(None)):
    """
    Returns simulated tracking timeline status for citizen reference number.
    Provides realistic demo records when testing.
    """
    ref_clean = (ref_number or "").strip()
    
    # Return matched demo record or default demo
    if ref_clean in TRACKING_DEMOS:
        data = TRACKING_DEMOS[ref_clean]
    elif "KMUT" in ref_clean.upper():
        data = TRACKING_DEMOS["TN-KMUT-2026-5510293"]
    else:
        data = TRACKING_DEMOS["TN-OAP-2026-8941029"]

    disclaimer_en = "This application progress tracker is an advisory guidance demonstration to help citizens understand official approval stages. It is not directly linked to official live state databases."
    disclaimer_ta = "இந்த விண்ணப்ப நிலை கண்காணிப்பு என்பது தாலுகா / அரசு அலுவலகApproval நிலைகளைப் புரிந்து கொள்ள உதவும் மாதிரி வழிகாட்டி மட்டுமே; அதிகாரப்பூர்வ அரசு நேரலை தளம் அல்ல."

    return ApplicationStatusResponse(
        reference_number=data["reference_number"],
        scheme_id=data["scheme_id"],
        scheme_name_en=data["scheme_name_en"],
        scheme_name_ta=data["scheme_name_ta"],
        applicant_name=data["applicant_name"],
        submission_date=data["submission_date"],
        current_status=data["current_status"],
        stages=[TrackingStage(**stg) for stg in data["stages"]],
        voice_summary_en=data["voice_summary_en"],
        voice_summary_ta=data["voice_summary_ta"],
        disclaimer_en=disclaimer_en,
        disclaimer_ta=disclaimer_ta
    )
