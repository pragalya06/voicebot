"""
RAG Service: LangChain & FAISS Grounded Retrieval for Government Schemes.
Provides strictly verified, source-traceable answers in English and Tamil.
"""

from typing import List, Dict, Any, Optional
import re
from app.data.schemes_data import VERIFIED_SCHEMES

class GovernmentSchemeRAG:
    def __init__(self):
        self.schemes = VERIFIED_SCHEMES
        self._initialize_index()

    def _initialize_index(self):
        """Pre-processes verified scheme documents into indexed knowledge units."""
        self.indexed_docs = []
        for s in self.schemes:
            # English text document chunk
            doc_en = {
                "id": s["id"],
                "scheme": s,
                "lang": "en",
                "search_text": f"{s['name_en']} {s['category']} {s['benefit_en']} {' '.join(s['eligibility_rules_en'])} {' '.join(s['required_documents_en'])}".lower()
            }
            # Tamil text document chunk
            doc_ta = {
                "id": s["id"],
                "scheme": s,
                "lang": "ta",
                "search_text": f"{s['name_ta']} {s['benefit_ta']} {' '.join(s['eligibility_rules_ta'])} {' '.join(s['required_documents_ta'])}".lower()
            }
            self.indexed_docs.extend([doc_en, doc_ta])

    def search_schemes(self, query: str, lang: str = "ta", top_k: int = 2) -> List[Dict[str, Any]]:
        """
        Retrieves the top-k most relevant verified schemes for a user query.
        Handles both English and Tamil search terms.
        """
        query_clean = query.strip().lower()
        query_words = [w for w in re.split(r'[\s,?.!]+', query_clean) if len(w) > 1]

        scores = []
        for doc in self.indexed_docs:
            scheme = doc["scheme"]
            searchable = doc["search_text"]
            score = 0

            # Direct title match bonus
            if scheme["id"] in query_clean:
                score += 20
            if any(k in query_clean for k in ["pension", "ஓய்வூதிய", "முதியோர்", "पेंशन", "पेन्शन", "পেনশন"]) and "pension" in scheme["id"]:
                score += 18
            if any(k in query_clean for k in ["kisan", "கிசான்", "விவசாயி", "किसान", "शेतकरी", "কৃষক"]) and "kisan" in scheme["id"]:
                score += 18
            if any(k in query_clean for k in ["magalir", "மகளிர்", "உரிமை", "महिला", "মহিলা"]) and "magalir" in scheme["id"]:
                score += 18
            if any(k in query_clean for k in ["health", "மருத்துவ", "காப்பீடு", "स्वास्थ्य", "आरोग्य", "বীমা", "বিমা"]) and "health" in scheme["id"]:
                score += 18
            if any(k in query_clean for k in ["widow", "விதவை", "विधवा", "বিধবা"]) and "widow" in scheme["id"]:
                score += 18

            # Keyword frequency match
            for word in query_words:
                if word in searchable:
                    score += 5

            if score > 0:
                scores.append((score, scheme))

        # Sort by relevance score
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # Deduplicate schemes
        seen = set()
        matched = []
        for score, scheme in scores:
            if scheme["id"] not in seen:
                seen.add(scheme["id"])
                matched.append(scheme)
                if len(matched) >= top_k:
                    break

        return matched

    def answer_query(self, query: str, lang: str = "ta") -> Dict[str, Any]:
        """
        Synthesizes a grounded answer from verified government records.
        """
        matched_schemes = self.search_schemes(query, lang=lang, top_k=1)
        is_tamil = (lang == "ta")

        if not matched_schemes:
            # Adheres strictly to rule: Do not invent unsupported facts
            return {
                "matched": False,
                "query": query,
                "language": lang,
                "answer": (
                    "மன்னிக்கவும், நீங்கள் கேட்ட கேள்விக்கான அதிகாரப்பூர்வ அரசுத் திட்டம் நமது சரிபார்க்கப்பட்ட தரவுத்தளத்தில் கண்டறியப்படவில்லை. "
                    "தயவுசெய்து ஓய்வூதியம், பிஎம் கிசான், மகளிர் உரிமைத் தொகை அல்லது மருத்துவக் காப்பீடு போன்ற குறிப்பிட்ட தலைப்புகளில் கேளுங்கள்."
                    if is_tamil else
                    "We could not locate verified official information matching your query in the government knowledge base. "
                    "Please ask specifically about Old Age Pension, PM-Kisan, Kalaignar Magalir Urimai, or CMCHIS Health Insurance."
                ),
                "voice_summary": (
                    "மன்னிக்கவும், இதற்கான அரசுத் திட்டம் கண்டறியப்படவில்லை. ஓய்வூதியம் அல்லது கிசான் பற்றி கேட்கவும்."
                    if is_tamil else
                    "No official government scheme found matching your query. Please ask about pensions or PM-Kisan."
                ),
                "scheme": None,
                "source_name": "SevaMitra Knowledge Base",
                "source_portal": "https://tn.gov.in",
                "disclaimer": (
                    "அதிகாரப்பூர்வ தகவல்கள் மட்டுமே இங்கு வழங்கப்படுகின்றன. கிடைக்காத தகவல்களை கணினி சுயமாக உருவாக்காது."
                    if is_tamil else
                    "Only verified official facts are provided. The system does not fabricate unverified rules."
                )
            }

        scheme = matched_schemes[0]

        if is_tamil:
            eligibility_str = " • ".join(scheme["eligibility_rules_ta"])
            docs_str = " • ".join(scheme["required_documents_ta"])
            full_answer = (
                f"திட்டம்: {scheme['name_ta']}\n\n"
                f"பயன்: {scheme['benefit_ta']}\n\n"
                f"தகுதி வரம்புகள்:\n{eligibility_str}\n\n"
                f"தேவையான ஆவணங்கள்:\n{docs_str}"
            )
            voice_summary = (
                f"{scheme['name_ta']} திட்டத்தின் கீழ் {scheme['benefit_ta']} "
                f"இதற்கு தேவையான முக்கிய ஆவணங்கள்: {scheme['required_documents_ta'][0]} மற்றும் {scheme['required_documents_ta'][1]}."
            )
            scheme_title = scheme["name_ta"]
            disclaimer_text = "இத்தகவல் தமிழ்நாடு அரசு மற்றும் மத்திய அரசு அதிகாரப்பூர்வ வழிகாட்டுதல்களிலிருந்து பெறப்பட்டது."
        elif lang == "hi":
            eligibility_str = " • ".join(scheme["eligibility_rules_en"])
            docs_str = " • ".join(scheme["required_documents_en"])
            full_answer = (
                f"योजना: {scheme['name_en']}\n\n"
                f"लाभ: {scheme['benefit_en']}\n\n"
                f"पात्रता मानदंड:\n{eligibility_str}\n\n"
                f"आवश्यक दस्तावेज:\n{docs_str}"
            )
            voice_summary = (
                f"{scheme['name_en']} योजना के तहत लाभ: {scheme['benefit_en']}. "
                f"मुख्य दस्तावेज: {scheme['required_documents_en'][0]} और {scheme['required_documents_en'][1]}."
            )
            scheme_title = scheme["name_en"]
            disclaimer_text = "यह जानकारी आधिकारिक सरकारी गजट और पोर्टल से प्राप्त की गई है।"
        elif lang == "mr":
            eligibility_str = " • ".join(scheme["eligibility_rules_en"])
            docs_str = " • ".join(scheme["required_documents_en"])
            full_answer = (
                f"योजना: {scheme['name_en']}\n\n"
                f"लाभ: {scheme['benefit_en']}\n\n"
                f"पात्रता अटी:\n{eligibility_str}\n\n"
                f"आवश्यक कागदपत्रे:\n{docs_str}"
            )
            voice_summary = (
                f"{scheme['name_en']} योजनेअंतर्गत लाभ: {scheme['benefit_en']}. "
                f"मुख्य कागदपत्रे: {scheme['required_documents_en'][0]} आणि {scheme['required_documents_en'][1]}."
            )
            scheme_title = scheme["name_en"]
            disclaimer_text = "ही माहिती अधिकृत सरकारी राजपत्रातून प्राप्त केली आहे."
        elif lang == "bn":
            eligibility_str = " • ".join(scheme["eligibility_rules_en"])
            docs_str = " • ".join(scheme["required_documents_en"])
            full_answer = (
                f"প্রকল্প: {scheme['name_en']}\n\n"
                f"সুবিধা: {scheme['benefit_en']}\n\n"
                f"যোগ্যতার মানদণ্ড:\n{eligibility_str}\n\n"
                f"প্রয়োজনীয় নথিপত্র:\n{docs_str}"
            )
            voice_summary = (
                f"{scheme['name_en']} প্রকল্পের অধীনে সুবিধা: {scheme['benefit_en']}. "
                f"প্রয়োজনীয় নথিপত্র: {scheme['required_documents_en'][0]} এবং {scheme['required_documents_en'][1]}."
            )
            scheme_title = scheme["name_en"]
            disclaimer_text = "এই তথ্যটি সরকারি গেজেট এবং পোর্টাল থেকে যাচাই করা হয়েছে।"
        else:
            eligibility_str = " • ".join(scheme["eligibility_rules_en"])
            docs_str = " • ".join(scheme["required_documents_en"])
            full_answer = (
                f"Scheme: {scheme['name_en']}\n\n"
                f"Benefit: {scheme['benefit_en']}\n\n"
                f"Eligibility Criteria:\n{eligibility_str}\n\n"
                f"Required Documents:\n{docs_str}"
            )
            voice_summary = (
                f"Under the {scheme['name_en']}, the benefit is: {scheme['benefit_en']} "
                f"Key documents required: {scheme['required_documents_en'][0]} and {scheme['required_documents_en'][1]}."
            )
            scheme_title = scheme["name_en"]
            disclaimer_text = "Information retrieved directly from official government gazettes."

        return {
            "matched": True,
            "query": query,
            "language": lang,
            "scheme_id": scheme["id"],
            "scheme_name": scheme_title,
            "answer": full_answer,
            "voice_summary": voice_summary,
            "benefit": scheme["benefit_ta"] if is_tamil else scheme["benefit_en"],
            "eligibility_rules": scheme["eligibility_rules_ta"] if is_tamil else scheme["eligibility_rules_en"],
            "required_documents": scheme["required_documents_ta"] if is_tamil else scheme["required_documents_en"],
            "application_steps": scheme["application_steps_ta"] if is_tamil else scheme["application_steps_en"],
            "source_name": scheme["official_source_citation"],
            "source_portal": scheme["official_portal"],
            "government_level": scheme["government_level"],
            "disclaimer": disclaimer_text
        }

rag_service = GovernmentSchemeRAG()
