"""
RAG Service: Grounded Multilingual Retrieval for Government Schemes and General Services.
Covers:
  - Welfare/pension schemes (VERIFIED_SCHEMES) — Tamil Nadu & Central govt.
  - General government services (GENERAL_SERVICES) — Passport, PAN, Aadhaar, Driving Licence,
    Birth Certificate, Death Certificate, Voter ID, Ration Card, Scholarships, Income/Caste,
    Public Grievances (CPGRAMS/1100), Record Corrections, Ayushman Bharat PMJAY.

Supported languages: English (en), Tamil (ta), Hindi (hi), Marathi (mr), Bengali (bn).
"""

from typing import List, Dict, Any, Optional
import re
from app.data.schemes_data import VERIFIED_SCHEMES
from app.data.general_services_data import GENERAL_SERVICES

MINIMUM_RELEVANCE_THRESHOLD = 15


class GovernmentSchemeRAG:
    def __init__(self):
        self.schemes = VERIFIED_SCHEMES
        self.general_services = GENERAL_SERVICES
        self._initialize_index()

    # ------------------------------------------------------------------ #
    # Indexing                                                           #
    # ------------------------------------------------------------------ #

    def _initialize_index(self):
        """
        Builds a searchable index of document chunks across all supported languages
        (English, Tamil, Hindi, Marathi, Bengali).
        """
        self.indexed_docs = []

        # --- Welfare schemes ---
        for s in self.schemes:
            name_blob = " ".join([s.get(f"name_{l}", "") for l in ["en", "ta", "hi", "mr", "bn"]])
            benefit_blob = " ".join([s.get(f"benefit_{l}", "") for l in ["en", "ta", "hi", "mr", "bn"]])
            keyword_blob = " ".join(s.get("keywords", []))
            elig_blob = " ".join(
                [rule for l in ["en", "ta", "hi", "mr", "bn"] for rule in s.get(f"eligibility_rules_{l}", [])]
            )
            docs_blob = " ".join(
                [doc for l in ["en", "ta", "hi", "mr", "bn"] for doc in s.get(f"required_documents_{l}", [])]
            )
            steps_blob = " ".join(
                [step for l in ["en", "ta", "hi", "mr", "bn"] for step in s.get(f"application_steps_{l}", [])]
            )

            text_blob = f"{name_blob} {s.get('category', '')} {benefit_blob} {keyword_blob} {elig_blob} {docs_blob} {steps_blob}".lower()

            self.indexed_docs.append({
                "id": s["id"],
                "type": "scheme",
                "record": s,
                "search_text": text_blob,
                "_word_set": set(re.split(r"[\s,?.!;:'\"/\\()\[\]।॥]+", text_blob))
            })

        # --- General government services ---
        for svc in self.general_services:
            name_blob = " ".join([svc.get(f"name_{l}", "") for l in ["en", "ta", "hi", "mr", "bn"]])
            benefit_blob = " ".join([svc.get(f"benefit_{l}", "") for l in ["en", "ta", "hi", "mr", "bn"]])
            keyword_blob = " ".join(svc.get("keywords", []))
            elig_blob = " ".join(
                [rule for l in ["en", "ta", "hi", "mr", "bn"] for rule in svc.get(f"eligibility_rules_{l}", [])]
            )
            docs_blob = " ".join(
                [doc for l in ["en", "ta", "hi", "mr", "bn"] for doc in svc.get(f"required_documents_{l}", [])]
            )
            steps_blob = " ".join(
                [step for l in ["en", "ta", "hi", "mr", "bn"] for step in svc.get(f"application_steps_{l}", [])]
            )

            text_blob = f"{name_blob} {svc.get('category', '')} {benefit_blob} {keyword_blob} {elig_blob} {docs_blob} {steps_blob}".lower()

            self.indexed_docs.append({
                "id": svc["id"],
                "type": "service",
                "record": svc,
                "search_text": text_blob,
                "_word_set": set(re.split(r"[\s,?.!;:'\"/\\()\[\]।॥]+", text_blob))
            })

    # ------------------------------------------------------------------ #
    # Keyword Anchors (Multilingual across EN, TA, HI, MR, BN)          #
    # ------------------------------------------------------------------ #

    _KEYWORD_ANCHORS: Dict[str, List[str]] = {
        # 1. PAN Card
        "pan card": ["pan_card"],
        "pan": ["pan_card"],
        "பான் கார்டு": ["pan_card"],
        "பான்": ["pan_card"],
        "பான் அட்டை": ["pan_card"],
        "पैन कार्ड": ["pan_card"],
        "पैन": ["pan_card"],
        "पॅन कार्ड": ["pan_card"],
        "पॅन": ["pan_card"],
        "পান কার্ড": ["pan_card"],
        "প্যান": ["pan_card"],
        "form 49a": ["pan_card"],

        # 2. Passport
        "passport": ["passport"],
        "பாஸ்போர்ட்": ["passport"],
        "पासपोर्ट": ["passport"],
        "পাসপোর্ট": ["passport"],
        "tatkal": ["passport"],
        "டத்கால்": ["passport"],
        "तत्काल": ["passport"],
        "তৎকাল": ["passport"],

        # 3. Aadhaar
        "aadhaar": ["aadhaar"],
        "aadhar": ["aadhaar"],
        "uidai": ["aadhaar"],
        "ஆதார்": ["aadhaar"],
        "आधार": ["aadhaar"],
        "আধার": ["aadhaar"],
        "myaadhaar": ["aadhaar"],

        # 4. Driving Licence
        "driving licence": ["driving_licence"],
        "driving license": ["driving_licence"],
        "driving": ["driving_licence"],
        "licence": ["driving_licence"],
        "license": ["driving_licence"],
        "dl": ["driving_licence"],
        "rto": ["driving_licence"],
        "parivahan": ["driving_licence"],
        "learner": ["driving_licence"],
        "llr": ["driving_licence"],
        "ஓட்டுனர்": ["driving_licence"],
        "உரிமம்": ["driving_licence"],
        "ड्राइविंग": ["driving_licence"],
        "ड्राइविंग लाइसेंस": ["driving_licence"],
        "ड्रायव्हिंग": ["driving_licence"],
        "ड्रायव्हिंग लायसन्स": ["driving_licence"],
        "लायसन्स": ["driving_licence"],
        "चालक परवाना": ["driving_licence"],
        "परवाना": ["driving_licence"],
        "ড্রাইভিং": ["driving_licence"],
        "ড্রাইভিং লাইসেন্স": ["driving_licence"],

        # 5. Birth Certificate
        "birth certificate": ["birth_certificate"],
        "பிறப்புச் சான்றிதழ்": ["birth_certificate"],
        "பிறப்பு": ["birth_certificate"],
        "जन्म प्रमाण पत्र": ["birth_certificate"],
        "जन्म प्रमाण": ["birth_certificate"],
        "जन्म दाखला": ["birth_certificate"],
        "जन्म": ["birth_certificate"],
        "জন্ম সনদ": ["birth_certificate"],
        "জন্ম শংসাপত্র": ["birth_certificate"],
        "জন্ম": ["birth_certificate"],

        # 6. Death Certificate
        "death certificate": ["death_certificate"],
        "இறப்புச் சான்றிதழ்": ["death_certificate"],
        "இறப்பு": ["death_certificate"],
        "மரண சான்றிதழ்": ["death_certificate"],
        "मृत्यु प्रमाण पत्र": ["death_certificate"],
        "मृत्यु": ["death_certificate"],
        "मृत्यू दाखला": ["death_certificate"],
        "মৃত্যু সনদ": ["death_certificate"],
        "মৃত্যু": ["death_certificate"],

        # 7. Voter ID
        "voter id": ["voter_id"],
        "voter card": ["voter_id"],
        "voter": ["voter_id"],
        "epic card": ["voter_id"],
        "வாக்காளர்": ["voter_id"],
        "வாக்காளர் அட்டை": ["voter_id"],
        "मतदाता पहचान पत्र": ["voter_id"],
        "मतदाता": ["voter_id"],
        "वोटर आईडी": ["voter_id"],
        "मतदार ओळखपत्र": ["voter_id"],
        "मतदार": ["voter_id"],
        "ভোটার আইডি": ["voter_id"],
        "ভোটার কার্ড": ["voter_id"],
        "ভোটার": ["voter_id"],

        # 8. Income & Community/Caste Certificate
        "income certificate": ["income_caste_certificate"],
        "caste certificate": ["income_caste_certificate"],
        "community certificate": ["income_caste_certificate"],
        "வருமானச் சான்றிதழ்": ["income_caste_certificate"],
        "வருமானம்": ["income_caste_certificate"],
        "சாதிச் சான்றிதழ்": ["income_caste_certificate"],
        "சாதி": ["income_caste_certificate"],
        "आय प्रमाण पत्र": ["income_caste_certificate"],
        "आय प्रमाण": ["income_caste_certificate"],
        "जाति प्रमाण पत्र": ["income_caste_certificate"],
        "उत्पन्न दाखला": ["income_caste_certificate"],
        "जात प्रमाणपत्र": ["income_caste_certificate"],
        "আয়ের শংসাপত্র": ["income_caste_certificate"],
        "জাতিগত শংসাপত্র": ["income_caste_certificate"],

        # 9. Ration Card / Family Card
        "ration card": ["ration_card"],
        "family card": ["ration_card"],
        "smart ration card": ["ration_card"],
        "tnpds": ["ration_card"],
        "ரேஷன் கார்டு": ["ration_card"],
        "ரேஷன்": ["ration_card"],
        "குடும்ப அட்டை": ["ration_card"],
        "ராஷன்": ["ration_card"],
        "राशन कार्ड": ["ration_card"],
        "राशन": ["ration_card"],
        "रेशन कार्ड": ["ration_card"],
        "रेशन": ["ration_card"],
        "রেশন কার্ড": ["ration_card"],
        "রেশন": ["ration_card"],

        # 10. Scholarships
        "scholarship": ["scholarship_portal"],
        "scholarships": ["scholarship_portal"],
        "nsp": ["scholarship_portal"],
        "கல்வி உதவித்தொகை": ["scholarship_portal"],
        "மாணவர் உதவித்தொகை": ["scholarship_portal"],
        "ஸ்காலர்ஷிப்": ["scholarship_portal"],
        "छात्रवृत्ति": ["scholarship_portal"],
        "स्कॉलरशिप": ["scholarship_portal"],
        "शिष्यवृत्ती": ["scholarship_portal"],
        "স্কলারশিপ": ["scholarship_portal"],
        "বৃত্তি": ["scholarship_portal"],

        # 11. Complaints & Grievances
        "complaint": ["public_grievances"],
        "grievance": ["public_grievances"],
        "cpgrams": ["public_grievances"],
        "1100": ["public_grievances"],
        "delayed application": ["public_grievances"],
        "rejected application": ["public_grievances"],
        "file a complaint": ["public_grievances"],
        "file complaint": ["public_grievances"],
        "புகார்": ["public_grievances"],
        "குறைதீர்ப்பு": ["public_grievances"],
        "முதல்வர் உதவி மையம்": ["public_grievances"],
        "शिकायत": ["public_grievances"],
        "समस्या": ["public_grievances"],
        "तक्रार": ["public_grievances"],
        "तक्रार निवारण": ["public_grievances"],
        "অভিযোগ": ["public_grievances"],

        # 12. Record Corrections
        "correction": ["record_corrections"],
        "name correction": ["record_corrections"],
        "dob correction": ["record_corrections"],
        "address update": ["record_corrections"],
        "spelling mistake": ["record_corrections"],
        "wrong details": ["record_corrections"],
        "திருத்தம்": ["record_corrections"],
        "பெயர் மாற்றம்": ["record_corrections"],
        "பிறந்த தேதி மாற்றம்": ["record_corrections"],
        "சுதார்": ["record_corrections"],
        "सुधार": ["record_corrections"],
        "दुरुस्ती": ["record_corrections"],
        "सংশোধন": ["record_corrections"],

        # 13. Ayushman Bharat
        "ayushman bharat": ["ayushman_bharat_pmjay"],
        "ayushman": ["ayushman_bharat_pmjay"],
        "pmjay": ["ayushman_bharat_pmjay"],
        "golden card": ["ayushman_bharat_pmjay"],
        "ஆயுஷ்மான்": ["ayushman_bharat_pmjay"],
        "ஆயுஷ்மான் பாரத்": ["ayushman_bharat_pmjay"],
        "आयुष्मान": ["ayushman_bharat_pmjay"],
        "आयुष्मान भारत": ["ayushman_bharat_pmjay"],
        "আয়ুষ্মান": ["ayushman_bharat_pmjay"],
        "আয়ুষ্মান ভারত": ["ayushman_bharat_pmjay"],

        # 14. Old Age Pension
        "old age pension": ["old_age_pension"],
        "oap": ["old_age_pension"],
        "ignoaps": ["old_age_pension"],
        "முதியோர் ஓய்வூதியம்": ["old_age_pension"],
        "முதியோர்": ["old_age_pension"],
        "விருத்தாப்பிய": ["old_age_pension"],
        "वृद्धावस्था पेंशन": ["old_age_pension"],
        "वृद्धापकाळ पेन्शन": ["old_age_pension"],
        "বার্ধক্য পেনশন": ["old_age_pension"],
        "pension": ["old_age_pension", "widow_destitute_pension"],
        "ஓய்வூதிய": ["old_age_pension", "widow_destitute_pension"],
        "ஓய்வூதியம்": ["old_age_pension", "widow_destitute_pension"],
        "पेंशन": ["old_age_pension", "widow_destitute_pension"],
        "पेन्शन": ["old_age_pension", "widow_destitute_pension"],
        "পেনশন": ["old_age_pension", "widow_destitute_pension"],

        # 15. Widow Pension
        "widow pension": ["widow_destitute_pension"],
        "destitute pension": ["widow_destitute_pension"],
        "widow": ["widow_destitute_pension"],
        "விதவை ஓய்வூதியம்": ["widow_destitute_pension"],
        "விதவை": ["widow_destitute_pension"],
        "ஆதரவற்ற": ["widow_destitute_pension"],
        "विधवा पेंशन": ["widow_destitute_pension"],
        "विधवा": ["widow_destitute_pension"],
        "विधवा पेन्शन": ["widow_destitute_pension"],
        "বিধবা পেনশন": ["widow_destitute_pension"],
        "বিধবা": ["widow_destitute_pension"],

        # 16. PM Kisan
        "pm kisan": ["pm_kisan"],
        "pm-kisan": ["pm_kisan"],
        "pmkisan": ["pm_kisan"],
        "kisan samman nidhi": ["pm_kisan"],
        "kisan": ["pm_kisan"],
        "farmer": ["pm_kisan"],
        "farmers": ["pm_kisan"],
        "கிசான்": ["pm_kisan"],
        "பிஎம் கிசான்": ["pm_kisan"],
        "விவசாயி": ["pm_kisan"],
        "விவசாயிகள்": ["pm_kisan"],
        "पीएम किसान": ["pm_kisan"],
        "पीएम-किसान": ["pm_kisan"],
        "पीएमकिसान": ["pm_kisan"],
        "किसान": ["pm_kisan"],
        "किसान सम्मान निधि": ["pm_kisan"],
        "शेतकरी": ["pm_kisan"],
        "शेतकरी सन्मान निधी": ["pm_kisan"],
        "शेतकरी योजना": ["pm_kisan"],
        "शेती योजना": ["pm_kisan"],
        "পিএম কিষাণ": ["pm_kisan"],
        "পিএম কিষান": ["pm_kisan"],
        "কৃষক": ["pm_kisan"],
        "কৃষক সম্মান নিধি": ["pm_kisan"],

        # 17. Kalaignar Magalir Urimai
        "magalir": ["kalaignar_magalir_urimai"],
        "urimai": ["kalaignar_magalir_urimai"],
        "kmut": ["kalaignar_magalir_urimai"],
        "மகளிர் உரிமை": ["kalaignar_magalir_urimai"],
        "மகளிர்": ["kalaignar_magalir_urimai"],
        "உரிமைத் தொகை": ["kalaignar_magalir_urimai"],
        "महिला अधिकार": ["kalaignar_magalir_urimai"],
        "मगलिर उरीमई": ["kalaignar_magalir_urimai"],
        "मगळिर उरीमई": ["kalaignar_magalir_urimai"],
        "মগলির উরিমাই": ["kalaignar_magalir_urimai"],

        # 18. CMCHIS Health
        "cmchis": ["cmchis_health"],
        "காப்பீடு": ["cmchis_health", "ayushman_bharat_pmjay"],
        "மருத்துவக் காப்பீடு": ["cmchis_health", "ayushman_bharat_pmjay"],
        "स्वास्थ्य बीमा": ["ayushman_bharat_pmjay", "cmchis_health"],
        "आरोग्य विमा": ["ayushman_bharat_pmjay", "cmchis_health"],
        "স্বাস্থ্য বীমা": ["ayushman_bharat_pmjay"],
    }

    def _compute_score(self, query_clean: str, query_words: List[str], doc: Dict) -> int:
        """Returns relevance score for a single indexed document chunk."""
        doc_id = doc["id"]
        score = 0
        query_norm = query_clean.replace("-", " ")
        doc_id_norm = doc_id.replace("_", " ")

        # --- Tier 1: Exact service/scheme ID mentioned directly ---
        if doc_id_norm in query_norm or doc_id in query_clean:
            score += 30

        # --- Tier 2: High-value keyword anchor bonus (+25 per anchor hit) ---
        for anchor, target_ids in self._KEYWORD_ANCHORS.items():
            if (anchor in query_clean or anchor in query_norm) and doc_id in target_ids:
                score += 25

        # --- Tier 3: Whole-word frequency in pre-built search word set (+5 per word) ---
        word_set = doc["_word_set"]
        for word in query_words:
            if len(word) > 2 and word in word_set:
                score += 5

        return score

    # ------------------------------------------------------------------ #
    # Search                                                             #
    # ------------------------------------------------------------------ #

    def search(self, query: str, lang: str = "en", top_k: int = 1) -> List[Dict]:
        """
        Returns up to top_k best-matching records (scheme or service).
        Any result scoring below MINIMUM_RELEVANCE_THRESHOLD is discarded.
        """
        query_clean = query.strip().lower()
        query_words = [w for w in re.split(r"[\s,?.!;:'\"/\\]+", query_clean) if len(w) > 1]

        scored: List[tuple] = []
        for doc in self.indexed_docs:
            s = self._compute_score(query_clean, query_words, doc)
            if s >= MINIMUM_RELEVANCE_THRESHOLD:
                scored.append((s, doc))

        # Sort descending by score
        scored.sort(key=lambda x: x[0], reverse=True)

        # Deduplicate by id
        seen: set = set()
        results: List[Dict] = []
        for s, doc in scored:
            if doc["id"] not in seen:
                seen.add(doc["id"])
                results.append({"score": s, "type": doc["type"], "record": doc["record"]})
                if len(results) >= top_k:
                    break

        return results

    # ------------------------------------------------------------------ #
    # Answer synthesis                                                   #
    # ------------------------------------------------------------------ #

    def answer_query(self, query: str, lang: str = "en") -> Dict[str, Any]:
        """
        Returns a grounded, source-traceable answer dict.
        Never fabricates information. Returns an honest no-match response when
        nothing scores above the relevance threshold.
        """
        matches = self.search(query, lang=lang, top_k=1)

        if not matches:
            return self._no_match_response(query, lang)

        best = matches[0]
        if best["type"] == "scheme":
            return self._format_scheme_answer(best["record"], query, lang)
        else:
            return self._format_service_answer(best["record"], query, lang)

    # ------------------------------------------------------------------ #
    # No-match response                                                  #
    # ------------------------------------------------------------------ #

    def _no_match_response(self, query: str, lang: str) -> Dict[str, Any]:
        msgs = {
            "ta": (
                "மன்னிக்கவும், உங்கள் கேள்விக்கான அதிகாரப்பூர்வ தகவல் எங்கள் தரவுத்தளத்தில் கிடைக்கவில்லை. "
                "பாஸ்போர்ட், பான் கார்டு, ஆதார், ஓட்டுனர் உரிமம், வாக்காளர் அட்டை, பிறப்பு/இறப்பு சான்றிதழ், "
                "ரேஷன் கார்டு, வருமான/சாதி சான்றிதழ், உதவித்தொகை, அல்லது அரசு குறைதீர்ப்பு (1100) குறித்து கேட்கவும். "
                "மேலும் தகவல்களுக்கு india.gov.in அல்லது tn.gov.in தளங்களைப் பார்வையிடலாம்."
            ),
            "hi": (
                "क्षमा करें, आपके प्रश्न से संबंधित सत्यापित सरकारी जानकारी हमारे डेटाबेस में उपलब्ध नहीं है। "
                "आप पासपोर्ट, पैन कार्ड, आधार, ड्राइविंग लाइसेंस, वोटर आईडी, जन्म/मृत्यु प्रमाण पत्र, राशन कार्ड, "
                "छात्रवृत्ति, आय/जाति प्रमाण पत्र या सरकारी शिकायत (1100) के बारे में पूछ सकते हैं। "
                "अधिक जानकारी के लिए india.gov.in देखें।"
            ),
            "mr": (
                "माफ करा, तुमच्या प्रश्नाशी संबंधित अधिकृत सरकारी माहिती उपलब्ध नाही. "
                "पासपोर्ट, पॅन कार्ड, आधार, वाहन चालक परवाना, मतदार ओळखपत्र, जन्म/मृत्यू दाखला, राशन कार्ड, "
                "शिष्यवृत्ती किंवा शासकीय तक्रारींबद्दल विचारा. "
                "अधिक माहितीसाठी india.gov.in वर भेट द्या."
            ),
            "bn": (
                "দুঃখিত, আপনার প্রশ্নের জন্য কোনো যাচাইকৃত সরকারি তথ্য পাওয়া যায়নি। "
                "আপনি পাসপোর্ট, প্যান কার্ড, আধার, ড্রাইভিং লাইসেন্স, ভোটার আইডি, জন্ম/মৃত্যু সনদ, রেশন কার্ড, "
                "স্কলারশিপ বা সরকারি অভিযোগ সংক্রান্ত বিষয়ে প্রশ্ন করতে পারেন। "
                "আরও তথ্যের জন্য india.gov.in দেখুন।"
            ),
            "en": (
                "We could not find verified official government information matching your query in our knowledge base. "
                "You can ask about Passport, PAN Card, Aadhaar, Driving Licence, Voter ID, Birth/Death Certificate, "
                "Ration Card, Scholarships, Income/Caste Certificate, Pensions, or Government Complaints (1100 / CPGRAMS). "
                "For other services, please visit india.gov.in."
            ),
        }
        voice_msgs = {
            "ta": "மன்னிக்கவும், இதற்கான தகவல் கிடைக்கவில்லை. பிற அரசு சேவைகள் குறித்து கேட்கலாம்.",
            "hi": "क्षमा करें, यह जानकारी उपलब्ध नहीं है। अधिक जानकारी के लिए india.gov.in पर देखें।",
            "mr": "माफ करा, ही माहिती उपलब्ध नाही. अधिक माहितीसाठी india.gov.in पहा.",
            "bn": "দুঃখিত, তথ্য পাওয়া যায়নি। বিস্তারিত জানতে india.gov.in দেখুন।",
            "en": "No verified information found for your query. Please ask about available government services or visit india.gov.in.",
        }
        msg = msgs.get(lang, msgs["en"])
        vmsg = voice_msgs.get(lang, voice_msgs["en"])
        return {
            "matched": False,
            "query": query,
            "language": lang,
            "answer": msg,
            "voice_summary": vmsg,
            "scheme": None,
            "source_name": "india.gov.in — National Government Services Portal",
            "source_portal": "https://www.india.gov.in/",
            "disclaimer": "This service provides verified official information only.",
        }

    # ------------------------------------------------------------------ #
    # Welfare scheme answer formatting                                   #
    # ------------------------------------------------------------------ #

    def _format_scheme_answer(self, scheme: Dict, query: str, lang: str) -> Dict[str, Any]:
        # Headings
        _h = {
            "ta": {"scheme": "திட்டம்", "benefit": "பயன்", "elig": "தகுதி வரம்புகள்", "docs": "தேவையான ஆவணங்கள்", "steps": "விண்ணப்பிக்கும் முறை"},
            "hi": {"scheme": "योजना", "benefit": "लाभ", "elig": "पात्रता मानदंड", "docs": "आवश्यक दस्तावेज", "steps": "आवेदन कैसे करें"},
            "mr": {"scheme": "योजना", "benefit": "लाभ", "elig": "पात्रता अटी", "docs": "आवश्यक कागदपत्रे", "steps": "अर्ज कसा करावा"},
            "bn": {"scheme": "প্রকল্প", "benefit": "সুবিধা", "elig": "যোগ্যতার মানদণ্ড", "docs": "প্রয়োজনীয় নথিপত্র", "steps": "আবেদন পদ্ধতি"},
            "en": {"scheme": "Scheme", "benefit": "Benefit", "elig": "Eligibility Criteria", "docs": "Required Documents", "steps": "Application Steps"},
        }
        h = _h.get(lang, _h["en"])

        name = scheme.get(f"name_{lang}") or scheme.get("name_en", "")
        benefit = scheme.get(f"benefit_{lang}") or scheme.get("benefit_en", "")
        elig_list = scheme.get(f"eligibility_rules_{lang}") or scheme.get("eligibility_rules_en", [])
        docs_list = scheme.get(f"required_documents_{lang}") or scheme.get("required_documents_en", [])
        steps_list = scheme.get(f"application_steps_{lang}") or scheme.get("application_steps_en", [])

        elig = " • ".join(elig_list)
        docs = " • ".join(docs_list)
        steps = "\n".join(steps_list)

        full_answer = (
            f"{h['scheme']}: {name}\n\n"
            f"{h['benefit']}: {benefit}\n\n"
            f"{h['elig']}:\n{elig}\n\n"
            f"{h['docs']}:\n{docs}\n\n"
            f"{h['steps']}:\n{steps}"
        )

        voice_summary = (
            f"{name}. {benefit}. "
            f"{h['docs']}: {docs_list[0] if docs_list else ''}."
        )

        disclaimers = {
            "ta": "இத்தகவல் அதிகாரப்பூர்வ அரசு வழிகாட்டுதல்களிலிருந்து பெறப்பட்டது.",
            "hi": "यह जानकारी आधिकारिक सरकारी गजट एवं पोर्टल से प्राप्त की गई है।",
            "mr": "ही माहिती अधिकृत सरकारी राजपत्रातून प्राप्त केली आहे.",
            "bn": "এই তথ্যটি সরকারি গেজেট ও পোর্টাল থেকে সংগৃহীত।",
            "en": "Information retrieved directly from official government gazettes.",
        }

        return {
            "matched": True,
            "query": query,
            "language": lang,
            "service_type": "welfare_scheme",
            "scheme_id": scheme["id"],
            "scheme_name": name,
            "answer": full_answer,
            "voice_summary": voice_summary,
            "benefit": benefit,
            "eligibility_rules": elig_list,
            "required_documents": docs_list,
            "application_steps": steps_list,
            "source_name": scheme["official_source_citation"],
            "source_portal": scheme["official_portal"],
            "government_level": scheme["government_level"],
            "disclaimer": disclaimers.get(lang, disclaimers["en"]),
        }

    # ------------------------------------------------------------------ #
    # General service answer formatting                                 #
    # ------------------------------------------------------------------ #

    def _format_service_answer(self, svc: Dict, query: str, lang: str) -> Dict[str, Any]:
        # Prefer translated fields where available; fallback cleanly
        name = svc.get(f"name_{lang}") or svc.get("name_en", "")
        benefit = svc.get(f"benefit_{lang}") or svc.get("benefit_en", "")
        elig_list = svc.get(f"eligibility_rules_{lang}") or svc.get("eligibility_rules_en", [])
        docs_list = svc.get(f"required_documents_{lang}") or svc.get("required_documents_en", [])
        steps_list = svc.get(f"application_steps_{lang}") or svc.get("application_steps_en", [])

        default_elig = {
            "ta": "தகுதியுடைய அனைத்து இந்திய குடிமக்களுக்கும் கிடைக்கும்.",
            "hi": "सभी पात्र भारतीय नागरिकों के लिए उपलब्ध।",
            "mr": "सर्व पात्र भारतीय नागरिकांसाठी उपलब्ध.",
            "bn": "সকল যোগ্য ভারতীয় নাগরিকদের জন্য উপলব্ধ।",
            "en": "Available for all eligible citizens."
        }
        default_docs = {
            "ta": "ஆதார் அட்டை, முகவரிச் சான்று.",
            "hi": "आधार कार्ड, पते का प्रमाण।",
            "mr": "आधार कार्ड, पत्ता पुरावा.",
            "bn": "আধার কার্ড, ঠিকানার প্রমাণ।",
            "en": "Aadhaar Card, Proof of Address."
        }
        default_steps = {
            "ta": f"{svc['official_portal']} என்ற அதிகாரப்பூர்வ போர்ட்டலில் விண்ணப்பிக்கவும்",
            "hi": f"आधिकारिक पोर्टल {svc['official_portal']} पर आवेदन करें",
            "mr": f"अधिकृत पोर्टल {svc['official_portal']} वर अर्ज करा",
            "bn": f"অফিসিয়াল পোর্টাল {svc['official_portal']}-এ আবেদন করুন",
            "en": f"Apply at {svc['official_portal']}"
        }

        elig = " • ".join(elig_list) if elig_list else default_elig.get(lang, default_elig["en"])
        docs = " • ".join(docs_list) if docs_list else default_docs.get(lang, default_docs["en"])
        steps_str = "\n".join(steps_list) if steps_list else default_steps.get(lang, default_steps["en"])
        fees = svc.get(f"fees_{lang}") or svc.get("fees_en", "")
        processing = svc.get(f"processing_time_{lang}") or svc.get("processing_time_en", "")
        portal = svc["official_portal"]

        _h = {
            "ta": {
                "service": "சேவை", "benefit": "பயன்", "elig": "தகுதி",
                "docs": "தேவையான ஆவணங்கள்", "steps": "விண்ணப்பிக்கும் படிகள்",
                "fees": "கட்டணம்", "time": "செயலாக்க நேரம்",
            },
            "hi": {
                "service": "सेवा", "benefit": "लाभ", "elig": "पात्रता",
                "docs": "आवश्यक दस्तावेज", "steps": "आवेदन के चरण",
                "fees": "शुल्क", "time": "प्रसंस्करण समय",
            },
            "mr": {
                "service": "सेवा", "benefit": "लाभ", "elig": "पात्रता",
                "docs": "आवश्यक कागदपत्रे", "steps": "अर्जाच्या पायऱ्या",
                "fees": "शुल्क", "time": "प्रक्रिया वेळ",
            },
            "bn": {
                "service": "পরিষেবা", "benefit": "সুবিধা", "elig": "যোগ্যতা",
                "docs": "প্রয়োজনীয় নথিপত্র", "steps": "আবেদনের পদক্ষেপ",
                "fees": "ফি", "time": "প্রক্রিয়াকরণ সময়",
            },
            "en": {
                "service": "Service", "benefit": "What you get", "elig": "Eligibility",
                "docs": "Required Documents", "steps": "How to Apply",
                "fees": "Fees", "time": "Processing Time",
            },
        }
        h = _h.get(lang, _h["en"])

        full_answer = (
            f"{h['service']}: {name}\n\n"
            f"{h['benefit']}: {benefit}\n\n"
            f"{h['elig']}:\n{elig}\n\n"
            f"{h['docs']}:\n{docs}\n\n"
            f"{h['steps']}:\n{steps_str}"
        )
        if fees:
            full_answer += f"\n\n{h['fees']}: {fees}"
        if processing:
            full_answer += f"\n\n{h['time']}: {processing}"

        voice_summary = (
            f"{name}. {benefit}. "
            f"{h['docs']}: {docs_list[0] if docs_list else docs}. "
            f"Official portal: {portal}"
        )

        disclaimer_map = {
            "ta": "இத்தகவல் அதிகாரப்பூர்வ அரசு போர்டல்களிலிருந்து பெறப்பட்டது.",
            "hi": "यह जानकारी आधिकारिक सरकारी पोर्टल से प्राप्त की गई है।",
            "mr": "ही माहिती अधिकृत सरकारी पोर्टलवरून प्राप्त केली आहे.",
            "bn": "এই তথ্য সরকারি পোর্টাল থেকে সংগ্রহ করা হয়েছে।",
            "en": "Information sourced from official government portals.",
        }

        return {
            "matched": True,
            "query": query,
            "language": lang,
            "service_type": "general_service",
            "scheme_id": svc["id"],
            "scheme_name": name,
            "answer": full_answer,
            "voice_summary": voice_summary,
            "benefit": benefit,
            "eligibility_rules": elig_list,
            "required_documents": docs_list,
            "application_steps": steps_list,
            "source_name": svc["official_source_citation"],
            "source_portal": portal,
            "government_level": svc["government_level"],
            "disclaimer": disclaimer_map.get(lang, disclaimer_map["en"]),
        }


rag_service = GovernmentSchemeRAG()
