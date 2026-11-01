"""
General Government Services Knowledge Base.
Covers official government services beyond welfare/pension schemes:
1. Passport
2. PAN Card
3. Aadhaar Card
4. Driving Licence
5. Birth Certificate
6. Death Certificate
7. Voter ID
8. Ayushman Bharat PMJAY
9. Income and Caste Certificates
10. Ration Card / Family Card
11. Scholarships (National Scholarship Portal)
12. Public Grievances and Complaints (CPGRAMS / CM Helpline 1100)
13. Correction of Records / Application Status & Appeals

All information is traceable to official state and central portals.
"""

GENERAL_SERVICES = [
    {
        "id": "passport",
        "name_en": "Indian Passport Application & Renewal",
        "name_ta": "இந்திய பாஸ்போர்ட் விண்ணப்பம் மற்றும் புதுப்பித்தல்",
        "name_hi": "भारतीय पासपोर्ट आवेदन एवं नवीनीकरण",
        "name_mr": "भारतीय पासपोर्ट अर्ज व नूतनीकरण",
        "name_bn": "ভারতীয় পাসপোর্ট আবেদন ও পুনর্নবীকরণ",
        "category": "Travel & Identity",
        "government_level": "Central Government (Ministry of External Affairs)",
        "official_portal": "https://www.passportindia.gov.in/",
        "official_source_citation": "Ministry of External Affairs, Passport Seva Programme",
        "keywords": [
            "passport", "passports", "travel document", "international travel",
            "visa", "apply passport", "renew passport", "tatkal",
            "பாஸ்போர்ட்", "வெளிநாடு", "டத்கால்", "விசா",
            "पासपोर्ट", "विदेश यात्रा", "तत्काल",
            "পাসপোর্ট", "বিদেশ ভ্রমণ", "তৎকাল",
            "पासपोर्ट", "परदेश प्रवास", "तत्काळ"
        ],
        "benefit_en": "Internationally valid travel document issued by Government of India, valid for 10 years (adults) or 5 years (minors). Enables international travel, visa applications, and serves as address and identity proof.",
        "benefit_ta": "இந்திய அரசால் வழங்கப்படும் சர்வதேச பயண ஆவணம். பெரியவர்களுக்கு 10 ஆண்டு, சிறியவர்களுக்கு 5 ஆண்டு செல்லும். சர்வதேச பயணம் மற்றும் அடையாளச் சான்றாக பயன்படுகிறது.",
        "benefit_hi": "भारत सरकार द्वारा जारी अंतरराष्ट्रीय यात्रा दस्तावेज, 10 वर्ष (वयस्क) या 5 वर्ष (नाबालिग) के लिए मान्य। विदेश यात्रा और पहचान प्रमाण के रूप में उपयोगी।",
        "benefit_mr": "भारत सरकारद्वारे जारी केलेले आंतरराष्ट्रीय प्रवास ओळखपत्र, प्रौढांसाठी १० वर्षे व अल्पवयीनांसाठी ५ वर्षे वैध. परदेश प्रवासासाठी आवश्यक.",
        "benefit_bn": "ভারত সরকার প্রদত্ত আন্তর্জাতিক ভ্রমণের নথি, প্রাপ্তবয়স্কদের জন্য ১০ বছর এবং অপ্রাপ্তবয়স্কদের জন্য ৫ বছর বৈধ।",
        "eligibility_rules_en": [
            "Any Indian citizen by birth or naturalization is eligible to apply.",
            "Minors require consent from parents (Annexure C/D).",
            "Fresh passport: No prior passport held.",
            "Re-issue: Existing passport expired/expiring within 1 year, or requires name/address change.",
            "Tatkal scheme: Urgent travel need; higher fee and expedited processing (1–3 days)."
        ],
        "eligibility_rules_ta": [
            "எந்த இந்திய குடிமகனும் விண்ணப்பிக்கலாம்.",
            "சிறார்களுக்கு பெற்றோரின் ஒப்புதல் தேவை.",
            "புதிய பாஸ்போர்ட்: முன்பு பாஸ்போர்ட் இல்லாதவர்கள்.",
            "மறுவழங்கல்: காலாவதியான அல்லது மாற்றங்கள் தேவைப்படும் பாஸ்போர்ட்.",
            "டத்கால்: அவசர பயண தேவை; கூடுதல் கட்டணம், விரைவு செயலாக்கம் (1–3 நாட்கள்)."
        ],
        "eligibility_rules_hi": [
            "कोई भी भारतीय नागरिक आवेदन करने के लिए पात्र है।",
            "नाबालिगों के लिए माता-पिता की सहमति आवश्यक है।",
            "नया पासपोर्ट: जिनके पास पहले पासपोर्ट नहीं था।",
            "पुनर्निर्गम: 1 वर्ष के भीतर समाप्त होने वाला या विवरण में बदलाव हेतु।",
            "तत्काल योजना: आपातकालीन यात्रा के लिए 1 से 3 दिनों में।"
        ],
        "eligibility_rules_mr": [
            "कोणताही भारतीय नागरिक अर्ज करू शकतो.",
            "अल्पवयीनांसाठी पालकांची संमती आवश्यक.",
            "नवीन पासपोर्ट: ज्यांच्याकडे आधी पासपोर्ट नव्हता.",
            "नूतनीकरण: मुदत संपलेला किंवा बदल करायचा असल्यास.",
            "तत्काळ: तातडीच्या प्रवासासाठी १ ते ३ दिवसांत."
        ],
        "eligibility_rules_bn": [
            "যে কোনো ভারতীয় নাগরিক আবেদন করতে পারেন।",
            "অপ্রাপ্তবয়স্কদের জন্য পিতামাতার সম্মতি আবশ্যক।",
            "নতুন পাসপোর্ট: পূর্বে পাসপোর্ট ছিল না এমন ব্যক্তিদের জন্য।",
            "পুনর্নবীকরণ: মেয়াদ শেষ হলে বা তথ্য পরিবর্তনের জন্য।",
            "তৎকাল: জরুরি ভ্রমণের ক্ষেত্রে ১ থেকে ৩ দিনে।"
        ],
        "required_documents_en": [
            "Proof of Identity: Aadhaar Card, Voter ID, PAN Card, or Driving Licence",
            "Proof of Address: Aadhaar Card, Electricity/Water bill, Bank Passbook",
            "Proof of Date of Birth: Birth Certificate, School Transfer Certificate (TC), or PAN",
            "Recent Passport Size Photographs (white background)",
            "Existing Passport (for re-issue / renewal)"
        ],
        "required_documents_ta": [
            "அடையாளச் சான்று: ஆதார், வாக்காளர் அட்டை, பான் அல்லது ஓட்டுனர் உரிமம்",
            "முகவரிச் சான்று: ஆதார், மின்சார/தண்ணீர் மசோதா, வங்கி கணக்கு புத்தகம்",
            "பிறந்த தேதி சான்று: பிறப்புச் சான்றிதழ், பள்ளி சான்று அல்லது பான் கார்டு",
            "பாஸ்போர்ட் அளவு புகைப்படங்கள் (வெள்ளை பின்னணி)",
            "தற்போதுள்ள பாஸ்போர்ட் (புதுப்பிப்புக்கு மட்டும்)"
        ],
        "required_documents_hi": [
            "पहचान प्रमाण: आधार कार्ड, वोटर आईडी, पैन कार्ड",
            "पता प्रमाण: आधार कार्ड, बिजली बिल, बैंक पासबुक",
            "जन्म तिथि प्रमाण: जन्म प्रमाण पत्र, स्कूल टीसी, पैन कार्ड",
            "पासपोर्ट साइज फोटो (सफेद पृष्ठभूमि)"
        ],
        "required_documents_mr": [
            "ओळख पुरावा: आधार कार्ड, मतदार ओळखपत्र, पॅन कार्ड",
            "पत्ता पुरावा: आधार कार्ड, वीज बिल, बँक पासबुक",
            "जन्म तारीख पुरावा: जन्म दाखला, शाळा सोडल्याचा दाखला, पॅन कार्ड",
            "पासपोर्ट आकाराचे फोटो"
        ],
        "required_documents_bn": [
            "পরিচয়ের প্রমাণ: আধার কার্ড, ভোটার আইডি, প্যান কার্ড",
            "ঠিকানার প্রমাণ: আধার কার্ড, বিদ্যুৎ বিল, ব্যাংক পাসবুক",
            "জন্মতারিখের প্রমাণ: জন্ম সনদ, স্কুল লিভিং সার্টিফিকেট, প্যান কার্ড",
            "পাসপোর্ট সাইজ ছবি"
        ],
        "application_steps_en": [
            "Step 1: Register at passportindia.gov.in and create an account.",
            "Step 2: Fill Form online (Fresh/Re-issue), pay fee via online payment.",
            "Step 3: Book appointment at nearest Passport Seva Kendra (PSK) or Post Office PSK.",
            "Step 4: Visit PSK with original documents for verification and biometric capture.",
            "Step 5: Police verification will be conducted at your address.",
            "Step 6: Passport delivered by Speed Post."
        ],
        "application_steps_ta": [
            "படி 1: passportindia.gov.in இல் பதிவு செய்து உள்நுழையவும்.",
            "படி 2: ஆன்லைன் விண்ணப்பப் படிவத்தை நிரப்பி கட்டணம் செலுத்தவும்.",
            "படி 3: அருகிலுள்ள பாஸ்போர்ட் சேவா கேந்திரா (PSK) இல் நேரம் முன்பதிவு செய்யவும்.",
            "படி 4: அசல் ஆவணங்களுடன் PSK சென்று ஆவண சரிபார்ப்பு மற்றும் கைரேகை பதிவு செய்யவும்.",
            "படி 5: உங்கள் முகவரிக்கு காவல்துறை சரிபார்ப்பு வரும்.",
            "படி 6: பாஸ்போர்ட் ஸ்பீட் போஸ்ட் மூலம் அனுப்பி வைக்கப்படும்."
        ],
        "application_steps_hi": [
            "चरण 1: passportindia.gov.in पर पंजीकरण करें।",
            "चरण 2: ऑनलाइन फॉर्म भरें और शुल्क भुगतान करें।",
            "चरण 3: नजदीकी पासपोर्ट सेवा केंद्र (PSK) में अपॉइंटमेंट बुक करें।",
            "चरण 4: मूल दस्तावेजों के साथ केंद्र में उपस्थित हों।",
            "चरण 5: पुलिस सत्यापन किया जाएगा।",
            "चरण 6: स्पीड पोस्ट से पासपोर्ट भेजा जाएगा।"
        ],
        "application_steps_mr": [
            "पायरी 1: passportindia.gov.in वर नोंदणी करा.",
            "पायरी 2: अर्ज भरा आणि ऑनलाइन शुल्क भरा.",
            "पायरी 3: जवळच्या पासपोर्ट सेवा केंद्राची अपॉइंटमेंट बुक करा.",
            "पायरी 4: मूळ कागदपत्रांसह केंद्रात उपस्थित राहा.",
            "पायरी 5: पोलीस पडताळणी होईल.",
            "पायरी 6: स्पीड पोस्टने पासपोर्ट घरी येईल."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: passportindia.gov.in-এ নিবন্ধন করুন।",
            "পদক্ষেপ ২: অনলাইন ফর্ম পূরণ করুন এবং ফি প্রদান করুন।",
            "পদক্ষেপ ৩: নিকটস্থ পাসপোর্ট সেবা কেন্দ্রে অ্যাপয়েন্টমেন্ট বুক করুন।",
            "পদক্ষেপ ৪: মূল নথিপত্র নিয়ে কেন্দ্রে যান।",
            "পদক্ষেপ ৫: পুলিশ ভেরিফিকেশন সম্পন্ন হবে।",
            "পদক্ষেপ ৬: স্পিড পোস্টের মাধ্যমে পাসপোর্ট পাঠানো হবে।"
        ],
        "fees_en": "Normal Fresh/Renewal (36 pages): ₹1,500. 60 pages: ₹2,000. Tatkal: additional ₹2,000. Minors: ₹1,000.",
        "processing_time_en": "Normal: 15–30 days. Tatkal: 1–3 days after PSK appointment."
    },
    {
        "id": "pan_card",
        "name_en": "PAN Card (Permanent Account Number)",
        "name_ta": "பான் கார்டு (நிரந்தர கணக்கு எண்)",
        "name_hi": "पैन कार्ड (स्थायी खाता संख्या)",
        "name_mr": "पॅन कार्ड (स्थायी खाते क्रमांक)",
        "name_bn": "প্যান কার্ড (স্থায়ী অ্যাকাউন্ট নম্বর)",
        "category": "Tax & Financial Identity",
        "government_level": "Central Government (Income Tax Department, NSDL/UTI)",
        "official_portal": "https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html",
        "official_source_citation": "Income Tax Department, Government of India",
        "keywords": [
            "pan card", "pan", "permanent account number", "income tax", "tax id",
            "pan apply", "new pan", "reprint pan", "pan correction", "form 49a",
            "பான்", "பான் கார்டு", "பான் அட்டை", "வருமான வரி அட்டை",
            "पैन", "पैन कार्ड", "स्थायी खाता संख्या", "आयकर",
            "पॅन", "पॅन कार्ड", "स्थायी खाते क्रमांक",
            "প্যান", "প্যান কার্ড", "স্থায়ী অ্যাকাউন্ট নম্বর"
        ],
        "benefit_en": "10-digit alphanumeric identifier required for opening bank accounts, income tax filing, financial transactions above ₹50,000, business registration, and valid national identity proof.",
        "benefit_ta": "வங்கி கணக்கு திறக்க, வருமான வரி தாக்கல் செய்ய, ₹50,000-க்கு மேற்பட்ட பரிவர்த்தனைகள் மற்றும் அடையாளச் சான்றுக்கான 10 இலக்க அரசு அடையாள அட்டை.",
        "benefit_hi": "बैंक खाता खोलने, आयकर रिटर्न भरने, 50,000 रुपये से अधिक के वित्तीय लेनदेन और पहचान प्रमाण के लिए 10 अंकों का विशिष्ट पहचान पत्र।",
        "benefit_mr": "बँक खाते उघडण्यासाठी, आयकर भरण्यासाठी आणि ५०,००० रुपयांपेक्षा जास्त व्यवहारांसाठी आवश्यक १० अंकी ओळख क्रमांक.",
        "benefit_bn": "ব্যাংক অ্যাকাউন্ট খোলা, আয়কর রিটার্ন জমা এবং ৫০,০০০ টাকার বেশি লেনদেনের জন্য প্রয়োজনীয় ১০ অঙ্কের পরিচয়পত্র।",
        "eligibility_rules_en": [
            "Any Indian citizen, NRI, or business entity is eligible.",
            "Mandatory for taxpayers, bank account holders, and businesses.",
            "Minors can apply through parent/guardian as representative assessee."
        ],
        "eligibility_rules_ta": [
            "எந்த இந்திய குடிமகனும், வெளிநாடு வாழ் இந்தியரும் அல்லது வணிக நிறுவனமும் விண்ணப்பிக்கலாம்.",
            "வரி செலுத்துவோர் மற்றும் வங்கி கணக்கு தொடங்குவோருக்கு கட்டாயம்.",
            "சிறார்களுக்கு பெற்றோரின் பிரதிநிதித்துவத்துடன் விண்ணப்பிக்கலாம்."
        ],
        "eligibility_rules_hi": [
            "कोई भी भारतीय नागरिक या व्यावसायिक इकाई पात्र है।",
            "करदाताओं और बैंक खाताधारकों के लिए अनिवार्य।",
            "नाबालिग माता-पिता के माध्यम से आवेदन कर सकते हैं।"
        ],
        "eligibility_rules_mr": [
            "कोणताही भारतीय नागरिक किंवा व्यावसायिक संस्था पात्र.",
            "करदाते व बँक खातेधारकांसाठी अनिवार्य."
        ],
        "eligibility_rules_bn": [
            "যে কোনো ভারতীয় নাগরিক বা ব্যবসায়িক প্রতিষ্ঠান যোগ্য।",
            "করদাতা এবং ব্যাংক অ্যাকাউন্টধারীদের জন্য বাধ্যতামূলক।"
        ],
        "required_documents_en": [
            "Proof of Identity: Aadhaar Card, Voter ID, Passport, or Driving Licence",
            "Proof of Address: Aadhaar Card, Electricity bill, Bank statement",
            "Proof of Date of Birth: Aadhaar Card, Birth Certificate, School Certificate",
            "Recent passport-size photographs (2 nos.)"
        ],
        "required_documents_ta": [
            "அடையாளச் சான்று: ஆதார், வாக்காளர் அட்டை, பாஸ்போர்ட்",
            "முகவரிச் சான்று: ஆதார், மின்சார மசோதா, வங்கி அறிக்கை",
            "பிறந்த தேதி சான்று: ஆதார் அட்டை அல்லது பிறப்புச் சான்றிதழ்",
            "பாஸ்போர்ட் அளவு புகைப்படங்கள் (2)"
        ],
        "required_documents_hi": [
            "पहचान प्रमाण: आधार कार्ड, वोटर आईडी, पासपोर्ट",
            "पता प्रमाण: आधार कार्ड, बिजली बिल, बैंक स्टेटमेंट",
            "जन्म तिथि प्रमाण: आधार कार्ड, जन्म प्रमाण पत्र",
            "पासपोर्ट साइज फोटो"
        ],
        "required_documents_mr": [
            "ओळख पुरावा: आधार कार्ड, मतदार ओळखपत्र",
            "पत्ता पुरावा: आधार कार्ड, वीज बिल",
            "जन्म तारीख पुरावा: आधार कार्ड, जन्म दाखला"
        ],
        "required_documents_bn": [
            "পরিচয়ের প্রমাণ: আধার কার্ড, ভোটার কার্ড",
            "ঠিকানার প্রমাণ: আধার কার্ড, বিদ্যুৎ বিল",
            "জন্মতারিখের প্রমাণ: আধার কার্ড, জন্ম সনদ"
        ],
        "application_steps_en": [
            "Step 1: Apply online at Protean (NSDL) or UTIITSL website (Form 49A).",
            "Step 2: Instant e-PAN using Aadhaar OTP at incometax.gov.in (free, paperless).",
            "Step 3: For physical card, fill online form, upload Aadhaar, pay ₹107.",
            "Step 4: Physical PAN card delivered by post within 10–15 working days.",
            "Step 5: Link PAN with Aadhaar at incometax.gov.in."
        ],
        "application_steps_ta": [
            "படி 1: Protean (NSDL) அல்லது UTIITSL இணையதளத்தில் படிவம் 49A நிரப்பவும்.",
            "படி 2: ஆதார் OTP உள்ளவர்கள் incometax.gov.in இல் உடனடி இ-பான் இலவசமாக 10 நிமிடத்தில் பெறலாம்.",
            "படி 3: அட்டை பெற ஆன்லைனில் விண்ணப்பித்து ₹107 கட்டணம் செலுத்தவும்.",
            "படி 4: 10–15 நாட்களில் பான் கார்டு தபால் மூலம் வரும்.",
            "படி 5: incometax.gov.in இல் பான் மற்றும் ஆதாறை இணைக்கவும்."
        ],
        "application_steps_hi": [
            "चरण 1: NSDL या UTIITSL पोर्टल पर फॉर्म 49A भरें।",
            "चरण 2: आधार OTP द्वारा incometax.gov.in पर तत्काल ई-पैन (मुफ्त) प्राप्त करें।",
            "चरण 3: फिजिकल कार्ड के लिए ₹107 शुल्क का भुगतान करें।",
            "चरण 4: 10 से 15 दिनों में डाक द्वारा कार्ड प्राप्त करें।"
        ],
        "application_steps_mr": [
            "पायरी 1: NSDL किंवा UTIITSL वर फॉर्म 49A भरा.",
            "पायरी 2: incometax.gov.in वर आधार OTP द्वारे मोफत त्वरित ई-पॅन मिळवा.",
            "पायरी 3: कार्डसाठी ₹107 शुल्क भरा.",
            "पायरी 4: १०-१५ दिवसांत पॅन कार्ड घरी येईल."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: NSDL বা UTIITSL পোর্টালে ফর্ম 49A পূরণ করুন।",
            "পদক্ষেপ ২: incometax.gov.in থেকে আধার OTP দিয়ে বিনামূল্যে ই-প্যান পান।",
            "পদক্ষেপ ৩: কার্ডের জন্য ১০৭ টাকা ফি দিন।",
            "পদক্ষেপ ৪: ১০-১৫ দিনে ডাকযোগে কার্ড আসবে।"
        ],
        "fees_en": "Instant e-PAN: Free at incometax.gov.in. Physical PAN card delivery: ₹107 (within India), ₹1,017 (abroad). Reprint: ₹50.",
        "processing_time_en": "Instant e-PAN: 10 minutes. Physical Card: 10–15 working days."
    },
    {
        "id": "aadhaar",
        "name_en": "Aadhaar Card Enrolment & Update",
        "name_ta": "ஆதார் அட்டை பதிவு மற்றும் புதுப்பிப்பு",
        "name_hi": "आधार कार्ड नामांकन एवं अपडेट",
        "name_mr": "आधार कार्ड नोंदणी व दुरुस्ती",
        "name_bn": "আধার কার্ড নথিভুক্তি ও আপডেট",
        "category": "Identity & Biometric",
        "government_level": "Central Government (UIDAI)",
        "official_portal": "https://uidai.gov.in/",
        "official_source_citation": "Unique Identification Authority of India (UIDAI)",
        "keywords": [
            "aadhaar", "aadhar", "uid", "unique id", "biometric id",
            "aadhaar update", "aadhaar address change", "aadhaar mobile link",
            "aadhaar enroll", "aadhaar card", "myaadhaar",
            "ஆதார்", "ஆதார் அட்டை", "ஆதார் திருத்தம்", "மொபைல் எண் இணைப்பு",
            "आधार", "आधार कार्ड", "आधार अपडेट", "मोबाइल लिंक",
            "आधार", "आधार दुरुस्ती", "पत्ता बदल",
            "আধার", "আধার কার্ড", "আধার আপডেট"
        ],
        "benefit_en": "12-digit unique biometric identification number issued by UIDAI. Serves as universal identity, essential for government DBT subsidies, banking, SIM cards, and scholarship transfers.",
        "benefit_ta": "UIDAI வழங்கும் 12 இலக்க தனிப்பட்ட பயோமெட்ரிக் அடையாள எண். அரசு நலத்திட்ட உதவிகள், வங்கி கணக்கு மற்றும் பொது சேவைகளுக்கு கட்டாயம்.",
        "benefit_hi": "UIDAI द्वारा जारी 12 अंकों की विशिष्ट बायोमेट्रिक पहचान संख्या। सरकारी सब्सिडी, बैंक खाते और सभी सेवाओं के लिए अनिवार्य।",
        "benefit_mr": "UIDAI द्वारे दिलेला १२ अंकी बायोमेट्रिक ओळख क्रमांक. सरकारी योजना व बँक खात्यासाठी आवश्यक.",
        "benefit_bn": "UIDAI প্রদত্ত ১২ অঙ্কের বায়োমেট্রিক পরিচয় নম্বর। সরকারি ভর্তুকি ও ব্যাংকিং পরিষেবার জন্য বাধ্যতামূলক।",
        "eligibility_rules_en": [
            "All residents residing in India for 182 days or more are eligible.",
            "Children under 5 get Baal Aadhaar (blue card, no biometrics until age 5).",
            "Mandatory biometric updates at age 5 and age 15 (free of cost)."
        ],
        "eligibility_rules_ta": [
            "இந்தியாவில் வசிக்கும் அனைத்து குடியிருப்பாளர்களும் தகுதியுடையவர்கள்.",
            "5 வயதுக்குட்பட்ட குழந்தைகளுக்கு பால் ஆதார் வழங்கப்படும்.",
            "5 மற்றும் 15 வயதில் கட்டாய பயோமெட்ரிக் புதுப்பிப்பு இலவசம்."
        ],
        "eligibility_rules_hi": [
            "भारत में रहने वाले सभी निवासी पात्र हैं।",
            "5 वर्ष से कम उम्र के बच्चों के लिए बाल आधार।",
            "5 और 15 वर्ष की आयु में बायोमेट्रिक अपडेट अनिवार्य व निःशुल्क है।"
        ],
        "eligibility_rules_mr": [
            "भारतातील सर्व नागरिक पात्र आहेत.",
            "५ आणि १५ वर्षांनंतर बायोमेट्रिक अपडेट मोफत व अनिवार्य."
        ],
        "eligibility_rules_bn": [
            "ভারতে বসবাসকারী সমস্ত নাগরিক যোগ্য।",
            "৫ এবং ১৫ বছর বয়সে বায়োমেট্রিক আপডেট বিনামূল্যে ও বাধ্যতামূলক।"
        ],
        "required_documents_en": [
            "Proof of Identity (POI): Voter ID, PAN Card, Passport, or Ration Card",
            "Proof of Address (POA): Electricity bill, Water bill, Ration card, or Bank Passbook",
            "Proof of Date of Birth (PDB): Birth Certificate, School mark sheet, or PAN"
        ],
        "required_documents_ta": [
            "அடையாளச் சான்று: வாக்காளர் அட்டை, பான், பாஸ்போர்ட்",
            "முகவரிச் சான்று: குடும்ப அட்டை, மின்சார மசோதா, வங்கி புத்தகம்",
            "பிறந்த தேதி சான்று: பிறப்புச் சான்றிதழ், பள்ளி சான்றிதழ்"
        ],
        "required_documents_hi": [
            "पहचान प्रमाण: वोटर आईडी, पैन कार्ड, पासपोर्ट",
            "पता प्रमाण: बिजली बिल, राशन कार्ड, बैंक पासबुक",
            "जन्म तिथि प्रमाण: जन्म प्रमाण पत्र, स्कूल अंकपत्र"
        ],
        "required_documents_mr": [
            "ओळख पुरावा: मतदार ओळखपत्र, पॅन कार्ड",
            "पत्ता पुरावा: वीज बिल, रेशन कार्ड, बँक पासबुक",
            "जन्म पुरावा: जन्म दाखला"
        ],
        "required_documents_bn": [
            "পরিচয় প্রমাণ: ভোটার আইডি, প্যান কার্ড",
            "ঠিকানার প্রমাণ: বিদ্যুৎ বিল, রেশন কার্ড",
            "জন্মের প্রমাণ: জন্ম সনদ"
        ],
        "application_steps_en": [
            "New Enrolment: Visit nearest Aadhaar Enrolment Centre / Bank / Post Office with documents.",
            "Biometrics (fingerprints, iris, facial photograph) captured at centre.",
            "Address update: Can be done online at myaadhaar.uidai.gov.in using supporting POA doc.",
            "Mobile number update: Requires in-person biometric verification at Aadhaar centre (cannot be done online without OTP).",
            "Download e-Aadhaar anytime free at myaadhaar.uidai.gov.in using OTP."
        ],
        "application_steps_ta": [
            "புதிய பதிவு: அசல் ஆவணங்களுடன் அருகிலுள்ள ஆதார் மையம் / வங்கி / தபால் நிலையம் செல்லவும்.",
            "கைரேகை, கண் கருவிழி மற்றும் புகைப்படம் எடுக்கப்படும்.",
            "முகவரி மாற்றம்: myaadhaar.uidai.gov.in வழியே ஆன்லைனில் செய்யலாம்.",
            "மொபைல் எண் மாற்றம்: ஆதார் மையத்திற்கு நேரில் சென்று கைரேகை வைத்து மட்டுமே மாற்ற முடியும்.",
            "இ-ஆதார் பதிவிறக்கம்: myaadhaar.uidai.gov.in இல் எப்போதும் இலவசமாக பதிவிறக்கம் செய்யலாம்."
        ],
        "application_steps_hi": [
            "नया नामांकन: नजदीकी आधार सेवा केंद्र, डाकघर या बैंक में जाएं।",
            "बायोमेट्रिक (उंगलियों के निशान, आंख की पुतली, फोटो) लिया जाएगा।",
            "पता अपडेट: myaadhaar.uidai.gov.in पर ऑनलाइन कर सकते हैं।",
            "मोबाइल नंबर अपडेट: आधार केंद्र जाकर बायोमेट्रिक से ही होगा।"
        ],
        "application_steps_mr": [
            "नवीन नोंदणी: जवळच्या आधार केंद्रात किंवा पोस्ट ऑफिसमध्ये जा.",
            "पत्ता बदल: myaadhaar.uidai.gov.in वर ऑनलाइन करता येतो.",
            "मोबाईल नंबर जोडणे: आधार केंद्रात जाऊन बायोमेट्रिक पडताळणी करावी लागते."
        ],
        "application_steps_bn": [
            "নতুন নথিভুক্তি: নিকটস্থ আধার কেন্দ্র বা পোস্ট অফিসে যান।",
            "ঠিকানা পরিবর্তন: myaadhaar.uidai.gov.in-এ অনলাইনে করা যায়।",
            "মোবাইল নম্বর লিঙ্ক: আধার কেন্দ্রে গিয়ে বায়োমেট্রিক দিয়ে করতে হবে।"
        ],
        "fees_en": "Fresh Enrolment: Free. Biometric update at age 5/15: Free. Demographic update (Name/Address): ₹50. Biometric update: ₹100. e-Aadhaar Download: Free.",
        "processing_time_en": "New Aadhaar: 15–90 days. Update: 5–30 days."
    },
    {
        "id": "driving_licence",
        "name_en": "Driving Licence & Learner's Licence",
        "name_ta": "ஓட்டுனர் உரிமம் மற்றும் கற்றல் உரிமம்",
        "name_hi": "ड्राइविंग लाइसेंस एवं लर्नर लाइसेंस",
        "name_mr": "वाहन चालक परवाना (ड्रायव्हिंग लायसन्स)",
        "name_bn": "ড্রাইভিং লাইসেন্স ও লার্নার লাইসেন্স",
        "category": "Transport & Motor Vehicles",
        "government_level": "State Government / MoRTH (Parivahan)",
        "official_portal": "https://parivahan.gov.in/parivahan/",
        "official_source_citation": "Ministry of Road Transport and Highways (Sarathi Parivahan)",
        "keywords": [
            "driving licence", "driving license", "dl", "driver licence",
            "learner licence", "learning licence", "rto", "motor vehicle",
            "bike licence", "two wheeler", "four wheeler", "renew dl",
            "ஓட்டுனர்", "ஓட்டுனர் உரிமம்", "கற்றல் உரிமம்", "எல்எல்ஆர்",
            "ड्राइविंग", "ड्राइविंग लाइसेंस", "लर्नर लाइसेंस", "आरटीओ",
            "चालक परवाना", "ड्रायव्हिंग लायसन्स", "आरटीओ",
            "ড্রাইভিং", "ড্রাইভিং লাইসেন্স", "লার্নার লাইসেন্স"
        ],
        "benefit_en": "Legal authorization to drive motor vehicles on Indian roads. Serves as a universally accepted government photo identity and address document.",
        "benefit_ta": "இந்திய சாலைகளில் மோட்டார் வாகனம் ஓட்ட சட்டப்பூர்வ அனுமதி அட்டை. நம்பகமான அரசு புகைப்பட அடையாளச் சான்றாக பயன்படுகிறது.",
        "benefit_hi": "सड़कों पर वाहन चलाने की कानूनी अनुमति। वैध सरकारी पहचान पत्र के रूप में मान्य।",
        "benefit_mr": "सार्वजनिक रस्त्यांवर वाहन चालवण्याचा कायदेशीर परवाना. अधिकृत ओळख पुरावा.",
        "benefit_bn": "যানবাহন চালানোর আইনি অনুমতিপত্র। বৈধ সরকারি পরিচয়পত্র হিসেবে গ্রহণযোগ্য।",
        "eligibility_rules_en": [
            "Age 18+ for motor vehicles with gear and four-wheelers.",
            "Age 16+ for gearless motorcycles below 50cc (parental consent needed).",
            "Age 20+ for commercial transport vehicles.",
            "Must hold Learner Licence (LLR) for at least 30 days before taking permanent DL test."
        ],
        "eligibility_rules_ta": [
            "கியர் உள்ள இருசக்கர மற்றும் நான்கு சக்கர வாகனங்களுக்கு 18 வயது பூர்த்தி.",
            "கியர் இல்லாத 50cc கீழ் உள்ள வாகனங்களுக்கு 16 வயது (பெற்றோர் அனுமதி).",
            "வணிக வாகனங்களுக்கு 20 வயது.",
            "நிரந்தர DL பெற குறைந்தது 30 நாட்கள் LLR வைத்திருக்க வேண்டும்."
        ],
        "eligibility_rules_hi": [
            "गियर वाले वाहन और चार पहिया के लिए न्यूनतम आयु 18 वर्ष।",
            "बिना गियर वाले वाहन (50cc से कम) के लिए 16 वर्ष।",
            "कमर्शियल वाहनों के लिए 20 वर्ष।",
            "स्थायी लाइसेंस के लिए कम से कम 30 दिन पुराना लर्नर लाइसेंस होना अनिवार्य।"
        ],
        "eligibility_rules_mr": [
            "गिअर असलेल्या वाहनांसाठी १८ वर्षे पूर्ण.",
            "पक्के लायसन्स काढण्यापूर्वी किमान ३० दिवस शिकाऊ (लर्नर) परवाना असणे आवश्यक."
        ],
        "eligibility_rules_bn": [
            "গিয়ারযুক্ত গাড়ির জন্য ন্যূনতম বয়স ১৮ বছর।",
            "স্থায়ী লাইসেন্সের জন্য কমপক্ষে ৩০ দিনের পুরোনো লার্নার লাইসেন্স থাকতে হবে।"
        ],
        "required_documents_en": [
            "Age Proof: Birth Certificate, School Transfer Certificate (TC), or PAN",
            "Address Proof: Aadhaar Card, Voter ID, or Utility bill",
            "Medical Certificate (Form 1A) for transport vehicles or applicants aged 40+",
            "Passport-size photographs",
            "Valid Learner's Licence (for permanent DL)"
        ],
        "required_documents_ta": [
            "வயதுச் சான்று: பிறப்புச் சான்றிதழ், பள்ளி சான்றிதழ் அல்லது பான்",
            "முகவரிச் சான்று: ஆதார் அட்டை, வாக்காளர் அட்டை",
            "மருத்துவச் சான்றிதழ் (படிவம் 1A) வணிக வாகனங்கள் அல்லது 40 வயதுக்கு மேற்பட்டோருக்கு",
            "பாஸ்போர்ட் அளவு புகைப்படங்கள்"
        ],
        "required_documents_hi": [
            "आयु प्रमाण: जन्म प्रमाण पत्र, स्कूल टीसी, पैन कार्ड",
            "पता प्रमाण: आधार कार्ड, वोटर आईडी",
            "पासपोर्ट साइज फोटो और मेडिकल फॉर्म 1A"
        ],
        "required_documents_mr": [
            "वय पुरावा: जन्म दाखला, शाळा सोडल्याचा दाखला",
            "पत्ता पुरावा: आधार कार्ड, वीज बिल"
        ],
        "required_documents_bn": [
            "বয়সের প্রমাণ: জন্ম সনদ, প্যান কার্ড",
            "ঠিকানার প্রমাণ: আধার কার্ড, ভোটার কার্ড"
        ],
        "application_steps_en": [
            "Step 1: Apply for Learner's Licence (LLR) online at parivahan.gov.in (Sarathi).",
            "Step 2: Upload Aadhaar for contactless, paperless LLR test from home in most states.",
            "Step 3: Pass simple road signs and safety rules computer test; download LLR.",
            "Step 4: Practice driving for 30 to 180 days.",
            "Step 5: Book driving test slot on parivahan.gov.in.",
            "Step 6: Pass physical driving test at RTO to receive permanent Smart Card DL."
        ],
        "application_steps_ta": [
            "படி 1: parivahan.gov.in சாரதி தளத்தில் LLR-க்கு ஆன்லைனில் விண்ணப்பிக்கவும்.",
            "படி 2: ஆதார் சரிபார்ப்பு மூலம் வீட்டிலிருந்தே கணினி வழி சாலை விதி தேர்வு எழுதலாம்.",
            "படி 3: தேர்ச்சி பெற்று கற்றல் உரிமத்தை (LLR) பதிவிறக்கவும்.",
            "படி 4: 30 நாட்கள் கழித்து நிரந்தர DL ஓட்டுனர் சோதனைக்கு நேரம் முன்பதிவு செய்யவும்.",
            "படி 5: RTO சென்று வாகன ஓட்டுனர் சோதனையில் தேர்ச்சி பெற்று ஸ்மார்ட் கார்டு DL பெறவும்."
        ],
        "application_steps_hi": [
            "चरण 1: parivahan.gov.in पर लर्नर लाइसेंस के लिए आवेदन करें।",
            "चरण 2: ऑनलाइन टेस्ट पास करके लर्नर लाइसेंस डाउनलोड करें।",
            "चरण 3: 30 दिन बाद स्थायी ड्राइविंग टेस्ट के लिए स्लॉट बुक करें।",
            "चरण 4: आरटीओ में ड्राइविंग टेस्ट पास करें और स्मार्ट कार्ड प्राप्त करें।"
        ],
        "application_steps_mr": [
            "पायरी 1: parivahan.gov.in वर शिकाऊ परवान्यासाठी अर्ज करा.",
            "पायरी 2: ऑनलाइन परीक्षा देऊन लर्नर लायसन्स मिळवा.",
            "पायरी 3: ३० दिवसांनंतर आरटीओ टेस्ट स्लॉट बुक करा.",
            "पायरी 4: आरटीओमध्ये ड्रायव्हिंग टेस्ट पास करून पक्के लायसन्स मिळवा."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: parivahan.gov.in পোর্টালে লার্নার লাইসেন্সের আবেদন করুন।",
            "পদক্ষেপ ২: অনলাইন টেস্ট দিয়ে লার্নার লাইসেন্স সংগ্রহ করুন।",
            "পদক্ষেপ ৩: ৩০ দিন পর স্থায়ী টেস্টের জন্য স্লট বুক করুন।",
            "পদক্ষেপ ৪: আরটিও-তে ড্রাইভ করে পাস করুন এবং স্মার্ট কার্ড পান।"
        ],
        "fees_en": "Learner Licence (LLR): ₹150 + test ₹50. Permanent DL: ₹200 + smart card ₹200. Renewal: ₹200.",
        "processing_time_en": "LLR: Same day (online). Permanent DL: 7–15 days after passing RTO test."
    },
    {
        "id": "voter_id",
        "name_en": "Voter ID Card (EPIC) & Voter Registration",
        "name_ta": "வாக்காளர் அடையாள அட்டை (EPIC) மற்றும் பதிவு",
        "name_hi": "मतदाता पहचान पत्र (वोटर आईडी) एवं पंजीकरण",
        "name_mr": "मतदार ओळखपत्र (वोटर आयडी) व नोंदणी",
        "name_bn": "ভোটার আইডি কার্ড ও ভোটার তালিকা নথিভুক্তি",
        "category": "Electoral & Civic Rights",
        "government_level": "Election Commission of India (ECI)",
        "official_portal": "https://voters.eci.gov.in/",
        "official_source_citation": "Election Commission of India",
        "keywords": [
            "voter id", "voter card", "election card", "epic card",
            "voter registration", "new voter", "form 6", "form 8", "eci",
            "வாக்காளர்", "வாக்காளர் அட்டை", "வாக்காளர் பதிவு", "படிவம் 6", "படிவம் 8",
            "मतदाता", "वोटर आईडी", "पहचान पत्र", "मतदाता पंजीकरण",
            "मतदार", "मतदार ओळखपत्र", "मतदान नोंदणी",
            "ভোটার", "ভোটার কার্ড", "ভোটার তালিকা"
        ],
        "benefit_en": "Electoral Photo Identity Card (EPIC) granting democratic voting rights in parliamentary, assembly, and local body elections. Widely accepted official address and photo ID proof.",
        "benefit_ta": "தேர்தலில் வாக்களிக்கும் அடிப்படை ஜனநாயக உரிமைக்கான அட்டை (EPIC). அனைத்து பொது சேவைகளுக்கும் அதிகாரப்பூர்வ அடையாள மற்றும் முகவரிச் சான்றாக பயன்படுகிறது.",
        "benefit_hi": "संसदीय व विधानसभा चुनावों में मतदान का संवैधानिक अधिकार देने वाला पहचान पत्र। आधिकारिक पते और पहचान का प्रमाण।",
        "benefit_mr": "निवडणुकीत मतदानाचा हक्क देणारे ओळखपत्र. पत्ता आणि ओळखीचा अधिकृत पुरावा.",
        "benefit_bn": "ভোটাধিকার প্রদানকারী পরিচয়পত্র। সরকারি ক্ষেত্রে ঠিকানা ও পরিচয়ের বৈধ প্রমাণ।",
        "eligibility_rules_en": [
            "Must be an Indian citizen aged 18 years or older on qualifying date (1st of Jan/Apr/Jul/Oct).",
            "Ordinary resident of the polling constituency."
        ],
        "eligibility_rules_ta": [
            "இந்திய குடிமகனாக இருக்க வேண்டும்; தகுதி நாளில் 18 வயது பூர்த்தியடைந்திருக்க வேண்டும்.",
            "குறிப்பிட்ட தொகுதியில் வசிப்பவராக இருக்க வேண்டும்."
        ],
        "eligibility_rules_hi": [
            "भारतीय नागरिक, जिसकी आयु 18 वर्ष या उससे अधिक हो।",
            "संबंधित निर्वाचन क्षेत्र का सामान्य निवासी हो।"
        ],
        "eligibility_rules_mr": [
            "वय १८ वर्षे पूर्ण असलेला भारतीय नागरिक.",
            "संबंधित मतदारसंघातील रहिवासी."
        ],
        "eligibility_rules_bn": [
            "১৮ বছর বা তার বেশি বয়সী ভারতীয় নাগরিক।",
            "সংশ্লিষ্ট নির্বাচনী এলাকার স্থায়ী বাসিন্দা।"
        ],
        "required_documents_en": [
            "Proof of Age: Birth Certificate, Aadhaar, School Leaving Certificate, or PAN",
            "Proof of Residence: Aadhaar, Electricity bill, Water bill, or Bank Passbook",
            "Passport-size photograph"
        ],
        "required_documents_ta": [
            "வயதுச் சான்று: பிறப்புச் சான்றிதழ், ஆதார், பள்ளி சான்று",
            "முகவரிச் சான்று: ஆதார், மின்சார மசோதா, குடும்ப அட்டை",
            "பாஸ்போர்ட் அளவு புகைப்படம்"
        ],
        "required_documents_hi": [
            "आयु प्रमाण: जन्म प्रमाण पत्र, आधार कार्ड, स्कूल प्रमाण पत्र",
            "निवास प्रमाण: आधार कार्ड, बिजली बिल, बैंक पासबुक",
            "पासपोर्ट साइज फोटो"
        ],
        "required_documents_mr": [
            "वय पुरावा: आधार कार्ड, जन्म दाखला",
            "पत्ता पुरावा: आधार कार्ड, वीज बिल"
        ],
        "required_documents_bn": [
            "বয়সের প্রমাণ: জন্ম সনদ, আধার কার্ড",
            "ঠিকানার প্রমাণ: আধার কার্ড, বিদ্যুৎ বিল"
        ],
        "application_steps_en": [
            "Step 1: Visit voters.eci.gov.in or download Voter Helpline App.",
            "Step 2: Fill Form 6 for new voter registration.",
            "Step 3: For correction or address change, fill Form 8.",
            "Step 4: Booth Level Officer (BLO) performs field verification.",
            "Step 5: EPIC number generated; download digital e-EPIC immediately.",
            "Step 6: Physical colour voter ID card delivered by Speed Post free of charge."
        ],
        "application_steps_ta": [
            "படி 1: voters.eci.gov.in செல்லவும் அல்லது Voter Helpline செயலியைப் பயன்படுத்தவும்.",
            "படி 2: புதிய வாக்காளர் பதிவுக்கு படிவம் 6-ஐ நிரப்பவும்.",
            "படி 3: முகவரி மாற்றம் அல்லது திருத்தத்திற்கு படிவம் 8-ஐ நிரப்பவும்.",
            "படி 4: வாக்குச்சாவடி நிலை அலுவலர் (BLO) முகவரியை சரிபார்ப்பார்.",
            "படி 5: வாக்காளர் எண் வந்ததும் டிஜிட்டல் e-EPIC பதிவிறக்கலாம்.",
            "படி 6: வண்ண வாக்காளர் அட்டை தபால் மூலம் இலவசமாக வீட்டிற்கு வரும்."
        ],
        "application_steps_hi": [
            "चरण 1: voters.eci.gov.in या वोटर हेल्पलाइन ऐप पर जाएं।",
            "चरण 2: नए पंजीकरण के लिए फॉर्म 6 भरें।",
            "चरण 3: सुधार या स्थानांतरण के लिए फॉर्म 8 भरें।",
            "चरण 4: बीएलओ (BLO) द्वारा सत्यापन किया जाएगा।",
            "चरण 5: ई-एपिक (e-EPIC) डाउनलोड करें और डाक से नया कार्ड प्राप्त करें।"
        ],
        "application_steps_mr": [
            "पायरी 1: voters.eci.gov.in किंवा व्होटर हेल्पलाइन ॲप उघडा.",
            "पायरी 2: नवीन नोंदणीसाठी फॉर्म ६ भरा; दुरुस्तीसाठी फॉर्म ८ भरा.",
            "पायरी 3: बीएलओद्वारे पडताळणी झाल्यानंतर मोफत स्पीड पोस्टने कार्ड घरी येईल."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: voters.eci.gov.in বা ভোটার হেল্পলাইন অ্যাপে যান।",
            "পদক্ষেপ ২: নতুন ভোটারদের জন্য ফর্ম ৬ এবং সংশোধনের জন্য ফর্ম ৮ পূরণ করুন।",
            "পদক্ষেপ ৩: বিএলও ভেরিফিকেশনের পর বিনামূল্যে স্পিড পোস্টে কার্ড পাবেন।"
        ],
        "fees_en": "100% Free of charge.",
        "processing_time_en": "Digital e-EPIC: 15–30 days. Physical Card Delivery: 30–45 days."
    },
    {
        "id": "birth_certificate",
        "name_en": "Birth Certificate Registration & Application",
        "name_ta": "பிறப்புச் சான்றிதழ் பதிவு மற்றும் விண்ணப்பம்",
        "name_hi": "जन्म प्रमाण पत्र पंजीकरण एवं आवेदन",
        "name_mr": "जन्म दाखला नोंदणी व अर्ज",
        "name_bn": "জন্ম সনদ নিবন্ধন ও আবেদন",
        "category": "Civil Registration & Documentation",
        "government_level": "State Government / Local Municipality / Panchayat",
        "official_portal": "https://crsorgi.gov.in/",
        "official_source_citation": "Office of the Registrar General of India, Civil Registration System (CRS)",
        "keywords": [
            "birth certificate", "birth proof", "date of birth certificate",
            "born certificate", "delivery certificate", "crs",
            "பிறப்பு", "பிறப்புச் சான்றிதழ்", "குழந்தை பிறப்பு",
            "जन्म", "जन्म प्रमाण पत्र", "जन्म दाखिला",
            "जन्म दाखला", "जन्म नोंदणी",
            "জন্ম", "জন্ম সনদ", "জন্ম শংসাপত্র"
        ],
        "benefit_en": "Primary legal proof of a person's birth, parentage, date, and place. Mandatory for school admissions, Aadhaar, Passport, PAN Card, and government scheme enrolments.",
        "benefit_ta": "ஒருவரின் பிறப்பு, தேதி, இடம் மற்றும் பெற்றோர் குறித்த முதன்மையான சட்டப்பூர்வ ஆவணம். பள்ளி சேர்க்கை, ஆதார், பாஸ்போர்ட் மற்றும் அனைத்து அரசு சலுகைகளுக்கும் அடிப்படை.",
        "benefit_hi": "जन्म, माता-पिता, तिथि और स्थान का प्राथमिक कानूनी प्रमाण। स्कूल प्रवेश, आधार, पासपोर्ट और सभी सरकारी योजनाओं के लिए अनिवार्य।",
        "benefit_mr": "जन्म, तारीख व ठिकाणाचा कायदेशीर पुरावा. शाळा प्रवेश, आधार व पासपोर्टसाठी अत्यंत आवश्यक.",
        "benefit_bn": "জন্মতারিখ, স্থান ও পিতামাতার পরিচয়ের প্রাথমিক আইনি প্রমাণ। স্কুল ভর্তি, আধার ও পাসপোর্টের জন্য আবশ্যক।",
        "eligibility_rules_en": [
            "Registration within 21 days of occurrence is free and standard.",
            "Delayed registration (21 to 30 days): late fee applies.",
            "30 days to 1 year: Requires permission from District Registrar / Revenue Officer.",
            "Beyond 1 year: Requires order from Executive Magistrate / Sub-Divisional Magistrate."
        ],
        "eligibility_rules_ta": [
            "பிறந்த 21 நாட்களுக்குள் பதிவு செய்வது இலவசம்.",
            "21 முதல் 30 நாட்களுக்குள் தாமதக் கட்டணத்துடன் பதிவு செய்யலாம்.",
            "1 வருடத்திற்கு மேற்பட்ட தாமதத்திற்கு வட்டாட்சியர் / நீதித்துறை உத்தரவு தேவை."
        ],
        "eligibility_rules_hi": [
            "जन्म के 21 दिनों के भीतर पंजीकरण निःशुल्क है।",
            "21 से 30 दिनों के भीतर विलंब शुल्क के साथ।",
            "1 वर्ष से अधिक की देरी पर मजिस्ट्रेट आदेश की आवश्यकता होती है।"
        ],
        "eligibility_rules_mr": [
            "जन्माच्या २१ दिवसांच्या आत नोंदणी मोफत.",
            "१ वर्षापेक्षा जास्त उशीर झाल्यास दंडाधिकारी आदेश आवश्यक."
        ],
        "eligibility_rules_bn": [
            "জন্মের ২১ দিনের মধ্যে নিবন্ধন বিনামূল্যে।",
            "১ বছরের বেশি দেরি হলে ম্যাজিস্ট্রেটের আদেশের প্রয়োজন হয়।"
        ],
        "required_documents_en": [
            "Hospital Discharge Slip / Proof of institutional delivery",
            "Parents' Aadhaar Cards",
            "Parents' Marriage Certificate (if available)",
            "Affidavit and local revenue report (for delayed registration over 1 year)"
        ],
        "required_documents_ta": [
            "மருத்துவமனை டிஸ்சார்ஜ் ரசீது / பிரசவ அறிக்கை",
            "பெற்றோரின் ஆதார் அட்டைகள்",
            "திருமணச் சான்று (இருப்பின்)"
        ],
        "required_documents_hi": [
            "अस्पताल डिस्चार्ज स्लिप / जन्म रिपोर्ट",
            "माता-पिता का आधार कार्ड",
            "विवाह प्रमाण पत्र (यदि हो)"
        ],
        "required_documents_mr": [
            "रुग्णालय डिस्चार्ज स्लिप / प्रसूती नोंद",
            "पालकांचे आधार कार्ड"
        ],
        "required_documents_bn": [
            "হাসপাতাল ডিসচার্জ সার্টিফিকেট",
            "পিতামাতার আধার কার্ড"
        ],
        "application_steps_en": [
            "Step 1: Institutional births are automatically registered by hospital on crsorgi.gov.in.",
            "Step 2: Collect certificate from Municipality / Town Panchayat / Village Panchayat office.",
            "Step 3: In Tamil Nadu, download digitally signed certificate directly from crsorgi.gov.in or e-Seva portal.",
            "Step 4: For child name inclusion, apply within 12 months at the local registrar office."
        ],
        "application_steps_ta": [
            "படி 1: மருத்துவமனைகளில் நிகழும் பிறப்புகள் crsorgi.gov.in தளத்தில் நேரடியாக பதிவு செய்யப்படும்.",
            "படி 2: நகராட்சி, பேரூராட்சி அல்லது கிராம ஊராட்சி அலுவலகத்தில் சான்றிதழ் பெறலாம்.",
            "படி 3: தமிழ்நாட்டில் crsorgi.gov.in அல்லது tn.gov.in தளத்தில் டிஜிட்டல் சான்றிதழை பதிவிறக்கலாம்.",
            "படி 4: குழந்தை பெயர் சேர்க்கை 12 மாதங்களுக்குள் இ-சேவை மூலம் செய்யலாம்."
        ],
        "application_steps_hi": [
            "चरण 1: अस्पताल में जन्म होने पर crsorgi.gov.in पर अस्पताल द्वारा स्वतः रिपोर्ट किया जाता है।",
            "चरण 2: स्थानीय नगर निगम या पंचायत कार्यालय से प्रमाण पत्र प्राप्त करें।",
            "चरण 3: आधिकारिक पोर्टल से डिजिटल प्रमाण पत्र डाउनलोड करें।"
        ],
        "application_steps_mr": [
            "पायरी 1: रुग्णालयातील जन्माची नोंद ग्रामपंचायत किंवा महानगरपालिकेकडे होते.",
            "पायरी 2: महापालिका किंवा ग्रामपंचायतीतून दाखला घ्या किंवा ऑनलाइन डाउनलोड करा."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: হাসপাতালে জন্ম হলে সরাসরি crsorgi বা স্বাস্থ্য দপ্তর থেকে রিপোর্ট হয়।",
            "পদক্ষেপ ২: পঞ্চায়েত বা পুরসভা কার্যালয় থেকে ডিজিটাল সনদ সংগ্রহ করুন।"
        ],
        "fees_en": "Within 21 days: Free. First copy usually free or nominal ₹10–₹25. Delayed registration: ₹20–₹100.",
        "processing_time_en": "Hospital registered: 7–15 days. Offline municipality: 15–30 days."
    },
    {
        "id": "death_certificate",
        "name_en": "Death Certificate Registration & Issuance",
        "name_ta": "இறப்புச் சான்றிதழ் பதிவு மற்றும் வழங்கல்",
        "name_hi": "मृत्यु प्रमाण पत्र पंजीकरण एवं निर्गमन",
        "name_mr": "मृत्यू दाखला नोंदणी व वाटप",
        "name_bn": "মৃত্যু সনদ নিবন্ধন ও আবেদন",
        "category": "Civil Registration & Legal Succession",
        "government_level": "State Government / Local Municipality / Panchayat",
        "official_portal": "https://crsorgi.gov.in/",
        "official_source_citation": "Office of the Registrar General of India, Civil Registration System",
        "keywords": [
            "death certificate", "death proof", "death registration", "demise certificate",
            "இறப்பு", "இறப்புச் சான்றிதழ்", "மரண சான்றிதழ்",
            "मृत्यु", "मृत्यु प्रमाण पत्र", "मृत्यु दाखिला",
            "मृत्यू दाखला", "मृत्यू नोंदणी",
            "মৃত্যু", "মৃত্যু সনদ", "মৃত্যু শংসাপত্র"
        ],
        "benefit_en": "Essential legal document confirming the death of a person. Mandatory for inheritance of property, bank account settlement, insurance claim disbursement, pension succession, and widow pension eligibility.",
        "benefit_ta": "ஒருவரின் மரணத்தை உறுதிப்படுத்தும் சட்டப்பூர்வ ஆவணம். சொத்து மாற்றம், வங்கி வைப்புத் தொகை பெறுதல், இன்சூரன்ஸ் இழப்பீடு, குடும்ப ஓய்வூதியம் மற்றும் விதவை ஓய்வூதியத்திற்கு கட்டாயம்.",
        "benefit_hi": "मृत्यु का आधिकारिक कानूनी प्रमाण। संपत्ति उत्तराधिकार, बैंक खाते के निपटान, बीमा दावों और पारिवारिक/विधवा पेंशन के लिए अनिवार्य।",
        "benefit_mr": "मृत्यूचा अधिकृत पुरावा. वारसा हक्क, बँक खाती, विमा रक्कम आणि पेन्शनसाठी अनिवार्य.",
        "benefit_bn": "মৃত্যুর বৈধ আইনি প্রমাণ। সম্পত্তির অধিকার, ব্যাংক দাবি, বীমার টাকা ও পারিবারিক পেনশনের জন্য আবশ্যক।",
        "eligibility_rules_en": [
            "Registration within 21 days of occurrence is standard and free.",
            "Reported by the head of the household or hospital authority.",
            "Delayed registration beyond 1 year requires order from Executive Magistrate / Revenue Divisional Officer (RDO)."
        ],
        "eligibility_rules_ta": [
            "இறந்த 21 நாட்களுக்குள் பதிவு செய்வது கட்டாயம் மற்றும் இலவசம்.",
            "மருத்துவமனை அல்லது குடும்பத் தலைவரால் பதிவு செய்யப்பட வேண்டும்.",
            "1 வருடத்திற்கு மேற்பட்ட தாமதத்திற்கு வருவாய் கோட்டாட்சியர் (RDO) உத்தரவு தேவை."
        ],
        "eligibility_rules_hi": [
            "मृत्यु के 21 दिनों के भीतर पंजीकरण अनिवार्य व निःशुल्क है।",
            "1 वर्ष से अधिक की देरी पर एसडीएम / आरडीओ की अनुमति आवश्यक।"
        ],
        "eligibility_rules_mr": [
            "२१ दिवसांच्या आत नोंदणी विनामूल्य.",
            "१ वर्षापेक्षा जास्त उशीर झाल्यास दंडाधिकारी आदेश आवश्यक."
        ],
        "eligibility_rules_bn": [
            "২১ দিনের মধ্যে নিবন্ধন করা বিনামূল্যে।",
            "১ বছরের বেশি সময় পার হলে প্রশাসনিক আদেশের প্রয়োজন।"
        ],
        "required_documents_en": [
            "Doctor's Medical Certificate of Cause of Death (Form 4/4A) or Cremation/Burial ground receipt",
            "Deceased person's Aadhaar Card / Voter ID",
            "Applicant's ID proof (relative / claimant)",
            "Ration Card of the family"
        ],
        "required_documents_ta": [
            "மருத்துவரின் இறப்பு காரண சான்றிதழ் அல்லது மயான ரசீது",
            "இறந்தவரின் ஆதார் அட்டை / வாக்காளர் அட்டை",
            "விண்ணப்பதாரரின் அடையாள அட்டை",
            "குடும்ப அட்டை"
        ],
        "required_documents_hi": [
            "चिकित्सक द्वारा मृत्यु कारण प्रमाण पत्र या श्मशान/कब्रिस्तान रसीद",
            "मृतक का आधार कार्ड",
            "आवेदक का पहचान पत्र"
        ],
        "required_documents_mr": [
            "डॉक्टरांचे प्रमाणपत्र किंवा स्मशानभूमी पावती",
            "मृत व्यक्तीचे आधार कार्ड",
            "अर्जदाराचे आधार कार्ड"
        ],
        "required_documents_bn": [
            "চিকিৎসকের মৃত্যুর কারণের সনদ বা শ্মশান/কবরস্থানের রসিদ",
            "মৃত ব্যক্তির আধার কার্ড",
            "আবেদনকারীর পরিচয়পত্র"
        ],
        "application_steps_en": [
            "Step 1: Obtain hospital cause of death slip or village VAO / burial report.",
            "Step 2: Submit report to Registrar of Births and Deaths (Municipality or Panchayat).",
            "Step 3: Collect certificate or download digitally signed copy from crsorgi.gov.in.",
            "Step 4: Use death certificate to apply for Legal Heir Certificate (Varisu Sanrithazh) via e-Seva."
        ],
        "application_steps_ta": [
            "படி 1: மருத்துவமனை இறப்பு அறிக்கை அல்லது மயான ரசீது / VAO அறிக்கை பெறவும்.",
            "படி 2: நகராட்சி அல்லது கிராம ஊராட்சி பிறப்பு-இறப்பு பதிவாளரிடம் சமர்ப்பிக்கவும்.",
            "படி 3: crsorgi.gov.in அல்லது இ-சேவை மையம் வழியே பதிவிறக்கம் செய்யவும்.",
            "படி 4: இறப்புச் சான்றிதழைக் கொண்டு வாரிசு சான்றிதழுக்கு (Legal Heir) இ-சேவையில் விண்ணப்பிக்கலாம்."
        ],
        "application_steps_hi": [
            "चरण 1: अस्पताल रिपोर्ट या श्मशान रसीद प्राप्त करें।",
            "चरण 2: नगर पालिका या ग्राम पंचायत रजिस्ट्रार को जमा करें।",
            "चरण 3: आधिकारिक पोर्टल से डिजिटल मृत्यु प्रमाण पत्र प्राप्त करें।"
        ],
        "application_steps_mr": [
            "पायरी 1: स्मशान पावती किंवा रुग्णालय अहवाल घ्या.",
            "पायरी 2: ग्रामपंचायत किंवा नगरपालिकेत नोंद करून दाखला मिळवा."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: হাসপাতাল বা শ্মশানের রিপোর্ট সংগ্রহ করুন।",
            "পদক্ষেপ ২: পঞ্চায়েত বা পুরসভায় জমা দিয়ে সনদ গ্রহণ করুন।"
        ],
        "fees_en": "Within 21 days: Free. Nominal copy fee ₹10–₹20.",
        "processing_time_en": "7–15 working days."
    },
    {
        "id": "income_caste_certificate",
        "name_en": "Income & Community/Caste Certificate",
        "name_ta": "வருமானச் சான்றிதழ் மற்றும் சாதிச் சான்றிதழ்",
        "name_hi": "आय एवं जाति प्रमाण पत्र",
        "name_mr": "उत्पन्न व जात प्रमाणपत्र",
        "name_bn": "আয় ও জাতিগত শংসাপত্র (Caste & Income Certificate)",
        "category": "Revenue & Welfare Prerequisites",
        "government_level": "State Revenue Department (Tahsildar / e-District / e-Seva)",
        "official_portal": "https://www.tnesevai.tn.gov.in/",
        "official_source_citation": "Revenue Department, Government of Tamil Nadu (e-District Portal)",
        "keywords": [
            "income certificate", "caste certificate", "community certificate",
            "obc certificate", "sc st certificate", "e-seva", "tahsildar", "revenue",
            "வருமானம்", "வருமானச் சான்றிதழ்", "சாதிச் சான்றிதழ்", "இ-சேவை", "தாசில்தார்",
            "आय प्रमाण", "आय प्रमाण पत्र", "जाति प्रमाण पत्र", "ई-डिस्ट्रिक्ट",
            "उत्पन्न दाखला", "जात प्रमाणपत्र", "तहसीलदार",
            "আয়ের শংসাপত্র", "জাতিগত শংসাপত্র", "কাস্ট সার্টিফিকেট"
        ],
        "benefit_en": "Official Revenue Department certificates proving annual family income and social community (SC/ST/OBC/BC). Essential prerequisites for pension schemes, fee waivers, scholarships, reservations, and subsidized government loans.",
        "benefit_ta": "குடும்ப ஆண்டு வருமானம் மற்றும் சமூகப் பிரிவை (SC/ST/OBC/MBC/BC) உறுதிப்படுத்தும் வருவாய்த் துறை சான்றிதழ். அரசு உதவித்தொகை, கல்லூரி கட்டண விலக்கு, இடஒதுக்கீடு மற்றும் ஓய்வூதியங்களுக்கு கட்டாயம்.",
        "benefit_hi": "पारिवारिक आय और सामाजिक वर्ग को प्रमाणित करने वाला राजस्व प्रमाण पत्र। छात्रवृत्ति, शुल्क छूट, सरकारी नौकरी आरक्षण और पेंशन योजनाओं के लिए अनिवार्य।",
        "benefit_mr": "वार्षिक उत्पन्न व सामाजिक जात प्रमाणित करणारा दाखला. शिष्यवृत्ती, सवलती आणि योजनांसाठी अत्यावश्यक.",
        "benefit_bn": "পারিবারিক আয় এবং সামাজিক বিভাগ প্রমাণকারী শংসাপত্র। সরকারি সুযোগ-সুবিধা, বৃত্তি ও সংরক্ষণের জন্য আবশ্যক।",
        "eligibility_rules_en": [
            "Resident of the state with verifiable family details.",
            "Income certificate valid for 1 financial year.",
            "Community/Caste certificate is a permanent document (does not expire)."
        ],
        "eligibility_rules_ta": [
            "மாநிலத்தில் வசிக்கும் குடும்பத்தினர் தகுதியுடையவர்கள்.",
            "வருமானச் சான்றிதழ் 1 நிதி ஆண்டுக்கு மட்டுமே செல்லும்.",
            "சாதிச் சான்றிதழ் நிரந்தரமானது (காலாவதி ஆகாது)."
        ],
        "eligibility_rules_hi": [
            "संबंधित राज्य का स्थायी निवासी।",
            "आय प्रमाण पत्र 1 वर्ष के लिए वैध; जाति प्रमाण पत्र स्थायी होता है।"
        ],
        "eligibility_rules_mr": [
            "राज्यातील कायमस्वरूपी रहिवासी.",
            "उत्पन्न दाखला १ वर्षासाठी, जात प्रमाणपत्र कायमस्वरूपी वैध."
        ],
        "eligibility_rules_bn": [
            "স্থায়ী বাসিন্দা হতে হবে।",
            "আয়ের শংসাপত্র ১ বছর বৈধ; জাতিগত সনদ স্থায়ী।"
        ],
        "required_documents_en": [
            "Aadhaar Card of applicant and parent/spouse",
            "Smart Ration Card (Family card)",
            "Salary Slip / Income Tax Return / Bank Passbook / Land Patta (for income proof)",
            "Parent's or Sibling's Community Certificate (for caste certificate)",
            "School Transfer Certificate (TC) showing caste",
            "Passport-size photograph"
        ],
        "required_documents_ta": [
            "விண்ணப்பதாரரின் ஆதார் அட்டை",
            "குடும்ப அட்டை (ஸ்மார்ட் கார்டு)",
            "சம்பள ரசீது அல்லது வங்கி கணக்கு புத்தகம் (வருமானத்திற்கு)",
            "பெற்றோர் அல்லது உடன்பிறந்தவர்களின் சாதிச் சான்றிதழ்",
            "பள்ளி மாற்றுச் சான்றிதழ் (TC)"
        ],
        "required_documents_hi": [
            "आधार कार्ड और राशन कार्ड",
            "आय का प्रमाण (वेतन पर्ची, बैंक पासबुक)",
            "माता-पिता या परिवार का जाति प्रमाण पत्र या स्कूल टीसी"
        ],
        "required_documents_mr": [
            "आधार कार्ड, रेशन कार्ड",
            "उत्पन्नाचा पुरावा (तलाठी दाखला / पगार पावती)",
            "वडिलांचा किंवा रक्ताच्या नातेवाईकांचा जात दाखला"
        ],
        "required_documents_bn": [
            "আধার কার্ড ও ডিজিটাল রেশন কার্ড",
            "আয়ের প্রমাণপত্র ও পরিবারের কারো জাতিগত শংসাপত্র"
        ],
        "application_steps_en": [
            "Step 1: Visit nearest e-Seva centre or apply online at tnesevai.tn.gov.in / state e-District portal.",
            "Step 2: Upload Aadhaar, Ration card, and income/parent community proofs.",
            "Step 3: Application routed to Village Administrative Officer (VAO) and Revenue Inspector (RI).",
            "Step 4: Field verification conducted.",
            "Step 5: Zonal Deputy Tahsildar / Tahsildar digitally approves certificate.",
            "Step 6: Download digitally signed PDF with QR code from portal or e-Seva centre."
        ],
        "application_steps_ta": [
            "படி 1: அருகிலுள்ள இ-சேவை (TNeGA) மையத்தை அணுகவும் அல்லது tnesevai.tn.gov.in இல் விண்ணப்பிக்கவும்.",
            "படி 2: ஆதார், குடும்ப அட்டை, பள்ளி TC பதிவேற்றவும்.",
            "படி 3: கிராம நிர்வாக அலுவலர் (VAO) மற்றும் வருவாய் ஆய்வாளர் (RI) ஆய்வு செய்வர்.",
            "படி 4: வட்டாட்சியர் (Tahsildar) டிஜிட்டல் கையொப்பமிட்டு ஒப்புதல் அளிப்பார்.",
            "படி 5: QR குறியீட்டுடன் கூடிய டிஜிட்டல் சான்றிதழை இ-சேவை மையத்தில் பதிவிறக்கம் செய்யலாம்."
        ],
        "application_steps_hi": [
            "चरण 1: नजदीकी ई-सेवा केंद्र (सीएससी) जाएं या ई-डिस्ट्रिक्ट पोर्टल पर आवेदन करें।",
            "चरण 2: दस्तावेज अपलोड करें। पटवारी/लेखपाल और तहसीलदार द्वारा सत्यापन होगा।",
            "चरण 3: ऑनलाइन डिजिटल हस्ताक्षरित प्रमाण पत्र डाउनलोड करें।"
        ],
        "application_steps_mr": [
            "पायरी 1: आपले सरकार सेवा केंद्रात (CSC) किंवा ऑनलाइन अर्ज करा.",
            "पायरी 2: तलाठी व मंडळ अधिकारी पडताळणीनंतर तहसीलदारांकडून डिजिटल दाखला मिळेल."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: ই-ডিস্ট্রিক্ট পোর্টাল বা বাংলা সহায়তা কেন্দ্রে আবেদন করুন।",
            "পদক্ষেপ ২: বিডিও বা এসডিও অফিস থেকে ভেরিফিকেশনের পর ডিজিটাল সনদ ডাউনলোড করুন।"
        ],
        "fees_en": "Government e-Seva application fee: ₹60 per certificate.",
        "processing_time_en": "10–15 working days."
    },
    {
        "id": "ration_card",
        "name_en": "Smart Ration Card / Family Card (PDS)",
        "name_ta": "ஸ்மார்ட் குடும்ப அட்டை / ரேஷன் கார்டு",
        "name_hi": "स्मार्ट राशन कार्ड (परिवार पहचान पत्र)",
        "name_mr": "स्मार्ट रेशन कार्ड (अन्नधान्य पत्रिका)",
        "name_bn": "ডিজিটাল রেশন কার্ড (Digital Ration Card)",
        "category": "Food Security & Family Identity",
        "government_level": "Civil Supplies & Consumer Protection Department",
        "official_portal": "https://www.tnpds.gov.in/",
        "official_source_citation": "Tamil Nadu Public Distribution System (TNPDS) / National Food Security Act (NFSA)",
        "keywords": [
            "ration card", "family card", "smart card", "smart ration card",
            "pds", "rice card", "tnpds", "add member", "address change ration",
            "ரேஷன்", "ரேஷன் கார்டு", "குடும்ப அட்டை", "ஸ்மார்ட் கார்டு", "உறுப்பினர் சேர்க்கை",
            "राशन", "राशन कार्ड", "खाद्य सुरक्षा", "नाम जोड़ना",
            "रेशन", "रेशन कार्ड", "अन्नपूर्णा", "नाव समाविष्ट",
            "রেশন", "রেশন কার্ড", "খাদ্যসাথী", "নাম সংশোধন"
        ],
        "benefit_en": "Subsidized food grains (free rice, wheat, sugar, dal) through Fair Price Shops under NFSA. Primary identity proof required for welfare pensions, Kalaignar Magalir Urimai, and health insurance.",
        "benefit_ta": "நியாயவிலைக் கடைகளில் இலவச அரிசி, சர்க்கரை, பருப்பு வழங்கும் உணவுப் பாதுகாப்பு அட்டை. மகளிர் உரிமைத் தொகை, ஓய்வூதியங்கள் மற்றும் அரசின் அனைத்து உதவிகளுக்கும் அடிப்படை.",
        "benefit_hi": "राष्ट्रीय खाद्य सुरक्षा के तहत मुफ्त या रियायती अनाज (चावल, गेहूं, चीनी)। सरकारी योजनाओं और पेंशन के लिए आवश्यक पारिवारिक दस्तावेज।",
        "benefit_mr": "रास्त भाव दुकानातून सवलतीच्या दरात अन्नधान्य मिळवण्यासाठी आवश्यक. सर्व शासकीय योजनांचा आधार.",
        "benefit_bn": "ন্যায্যমূল্যের দোকান থেকে বিনামূল্যে চাল, গম পাওয়ার ডিজিটাল কার্ড। সরকারি প্রকল্পের জন্য মূল ভিত্তি।",
        "eligibility_rules_en": [
            "Head of household and family members must be Indian citizens residing in the state.",
            "Family members must not be enrolled in another active ration card.",
            "Aadhaar seeding mandatory for all members."
        ],
        "eligibility_rules_ta": [
            "குடும்ப உறுப்பினர்கள் அனைவரும் மாநிலத்தில் வசிப்பவராக இருக்க வேண்டும்.",
            "வேறு எந்த குடும்ப அட்டையிலும் பெயர் இடம்பெற்றிருக்கக் கூடாது.",
            "அனைத்து உறுப்பினர்களுக்கும் ஆதார் எண் இணைக்கப்பட்டிருக்க வேண்டும்."
        ],
        "eligibility_rules_hi": [
            "राज्य के निवासी हों।",
            "किसी अन्य सक्रिय राशन कार्ड में नाम दर्ज न हो।",
            "सभी सदस्यों का आधार लिंक होना अनिवार्य।"
        ],
        "eligibility_rules_mr": [
            "राज्यातील रहिवासी.",
            "इतर रेशन कार्डात नाव नसावे व सर्वांचे आधार लिंक असावे."
        ],
        "eligibility_rules_bn": [
            "স্থায়ী বাসিন্দা হতে হবে এবং আধার লিংক বাধ্যতামূলক।"
        ],
        "required_documents_en": [
            "Aadhaar Cards of all family members",
            "Proof of Residence: Electricity bill, Gas connection receipt, or Registered Rent deed",
            "Marriage certificate or Removal certificate from parent's card (for new card after marriage)",
            "Birth certificate or Aadhaar for children",
            "Head of household photograph"
        ],
        "required_documents_ta": [
            "அனைத்து குடும்ப உறுப்பினர்களின் ஆதார் அட்டைகள்",
            "முகவரிச் சான்று: மின்சார மசோதா, கேஸ் ரசீது",
            "முந்தைய கார்டில் இருந்து பெயர் நீக்கப்பட்ட சான்று (பெயர் நீக்கல் சான்று)",
            "குழந்தைகளின் பிறப்புச் சான்றிதழ்"
        ],
        "required_documents_hi": [
            "परिवार के सभी सदस्यों का आधार कार्ड",
            "निवास प्रमाण: बिजली बिल, गैस कनेक्शन",
            "पुराने राशन कार्ड से नाम हटाने का प्रमाण पत्र (यदि लागू हो)"
        ],
        "required_documents_mr": [
            "कुटुंबातील सर्वांचे आधार कार्ड, वीज बिल, गॅस पावती"
        ],
        "required_documents_bn": [
            "সকল সদস্যের আধার কার্ড ও বিদ্যুৎ বিল"
        ],
        "application_steps_en": [
            "Step 1: Apply online at tnpds.gov.in or nearest e-Seva centre.",
            "Step 2: Upload Aadhaar of all members, address proof, and family photo.",
            "Step 3: Verification conducted by Taluk Supply Officer (TSO) / Inspector.",
            "Step 4: Smart Card printed and delivered via Taluk office or Fair Price Shop.",
            "Step 5: For member addition/deletion, use self-service portal tnpds.gov.in directly."
        ],
        "application_steps_ta": [
            "படி 1: tnpds.gov.in இணையதளத்தில் அல்லது இ-சேவை மையத்தில் ஆன்லைனில் விண்ணப்பிக்கவும்.",
            "படி 2: ஆதார் அட்டைகள், கேஸ் ரசீது, புகைப்படத்தை பதிவேற்றவும்.",
            "படி 3: வட்ட வழங்கல் அலுவலர் (TSO) கள ஆய்வு செய்வார்.",
            "படி 4: ஸ்மார்ட் கார்டு அச்சிடப்பட்டு நியாயவிலைக் கடையில் வழங்கப்படும்.",
            "படி 5: பெயர் சேர்க்கை, நீக்கம், முகவரி மாற்றத்தை tnpds.gov.in தளத்திலேயே எளிதாக செய்யலாம்."
        ],
        "application_steps_hi": [
            "चरण 1: राज्य के खाद्य पोर्टल (जैसे tnpds.gov.in) पर आवेदन करें।",
            "चरण 2: आपूर्ति निरीक्षक द्वारा सत्यापन किया जाएगा।",
            "चरण 3: स्मार्ट राशन कार्ड राशन डीलर या तहसील से प्राप्त करें।"
        ],
        "application_steps_mr": [
            "पायरी 1: अन्न व नागरी पुरवठा पोर्टलवर ऑनलाइन अर्ज करा.",
            "पायरी 2: पुरवठा निरीक्षकांच्या पडताळणीनंतर रेशन कार्ड उपलब्ध होईल."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: খাদ্য দপ্তরের পোর্টালে অনলাইন ফর্ম পূরণ করুন।",
            "পদক্ষেপ ২: পরিদর্শনের পর ডিজিটাল রেশন কার্ড পাবেন।"
        ],
        "fees_en": "Application: Free online. Smart Card printing: ₹20–₹50 at Taluk office.",
        "processing_time_en": "15–30 working days."
    },
    {
        "id": "scholarship_portal",
        "name_en": "National Scholarship Portal (NSP) & State Scholarships",
        "name_ta": "தேசிய கல்வி உதவித்தொகை போர்டல் (NSP) மற்றும் மாநில உதவித்தொகை",
        "name_hi": "राष्ट्रीय छात्रवृत्ति पोर्टल (NSP) एवं राज्य छात्रवृत्तियां",
        "name_mr": "राष्ट्रीय शिष्यवृत्ती पोर्टल (NSP) व राज्य शिष्यवृत्ती",
        "name_bn": "জাতীয় বৃত্তি পোর্টাল (NSP) ও সরকারি স্কলারশিপ",
        "category": "Education & Student Financial Support",
        "government_level": "Central & State Governments (MoE, MoMA, MoSJE)",
        "official_portal": "https://scholarships.gov.in/",
        "official_source_citation": "Ministry of Electronics & Information Technology, Government of India (NSP)",
        "keywords": [
            "scholarship", "scholarships", "nsp", "national scholarship portal",
            "post matric", "pre matric", "merit scholarship", "student aid",
            "கல்வி உதவித்தொகை", "மாணவர் உதவித்தொகை", "ஸ்காலர்ஷிப்", "படிப்பறிவு",
            "छात्रवृत्ति", "स्कॉलरशिप", "विद्यार्थी सहायता", "पोस्ट मैट्रिक",
            "शिष्यवृत्ती", "विद्यार्थी मदत", "मॅट्रिकपूर्व शिष्यवृत्ती",
            "স্কলারশিপ", "বৃত্তি", "ছাত্রবৃত্তি"
        ],
        "benefit_en": "Financial assistance covering tuition fees, maintenance allowance, and book grants directly credited to students' Aadhaar-seeded bank accounts through DBT for school, college, and university education.",
        "benefit_ta": "பள்ளி, கல்லூரி மற்றும் பல்கலைக்கழக மாணவர்களின் கல்விக் கட்டணம், தங்குமிடம் மற்றும் புத்தகச் செலவுகளுக்கு அரசு வழங்கும் நேரடி வங்கி நிதி உதவி (DBT).",
        "benefit_hi": "छात्रों के बैंक खाते में प्रत्यक्ष लाभ अंतरण (DBT) के माध्यम से शिक्षण शुल्क, छात्रावास और पुस्तकों के लिए वित्तीय सहायता।",
        "benefit_mr": "शाळा, महाविद्यालयीन विद्यार्थ्यांच्या शिक्षण व राहण्याच्या खर्चासाठी थेट बँक खात्यात शिष्यवृत्ती रक्कम.",
        "benefit_bn": "ছাত্রছাত্রীদের পড়াশোনার খরচ ও বৃত্তির টাকা সরাসরি ব্যাংক অ্যাকাউন্টে হস্তান্তরের সুবিধা।",
        "eligibility_rules_en": [
            "Enrolled in a recognized school, college, or university.",
            "Family annual income limits: Pre-matric: up to ₹1–₹2.5 Lakh; Post-matric: up to ₹2.5 Lakh; Top class: up to ₹6–₹8 Lakh.",
            "Minimum 50% marks in previous final examination (for merit categories).",
            "Target groups: SC, ST, OBC, Minority, Differently-abled, and Economically Weaker Sections."
        ],
        "eligibility_rules_ta": [
            "அங்கீகரிக்கப்பட்ட பள்ளி அல்லது கல்லூரியில் பயிலும் மாணவராக இருக்க வேண்டும்.",
            "குடும்ப ஆண்டு வருமானம் ₹2.5 லட்சத்திற்குள் இருக்க வேண்டும் (திட்டத்தைப் பொறுத்து).",
            "முந்தைய தேர்வில் குறைந்தபட்சம் 50% மதிப்பெண்கள் பெற்றிருக்க வேண்டும்."
        ],
        "eligibility_rules_hi": [
            "मान्यता प्राप्त संस्थान में अध्ययनरत छात्र।",
            "पारिवारिक वार्षिक आय ₹2.5 लाख तक।",
            "पिछली परीक्षा में न्यूनतम 50% अंक (मेरिट योजनाओं के लिए)।"
        ],
        "eligibility_rules_mr": [
            "मान्यताप्राप्त शाळा किंवा कॉलेजमध्ये शिक्षण घेणारे विद्यार्थी.",
            "वार्षिक उत्पन्न २.५ लाखांपर्यंत."
        ],
        "eligibility_rules_bn": [
            "স্বীকৃত স্কুল বা কলেজের নিয়মিত শিক্ষার্থী হতে হবে।"
        ],
        "required_documents_en": [
            "Student Aadhaar Card (with Aadhaar-seeded active bank account)",
            "Previous Year Academic Marksheet",
            "Current Year Fee Receipt / Bonafide Student Certificate from College",
            "Income Certificate issued by Revenue Authority",
            "Community / Caste / Minority Certificate",
            "Bank Passbook copy showing IFSC code and Account Number"
        ],
        "required_documents_ta": [
            "மாணவரின் ஆதார் அட்டை (வங்கியுடன் இணைக்கப்பட்டது)",
            "முந்தைய ஆண்டு மதிப்பெண் பட்டியல்",
            "கல்லூரி சேர்க்கை மற்றும் கட்டண ரசீது / Bonafide சான்று",
            "வருமானச் சான்றிதழ் மற்றும் சாதிச் சான்றிதழ்",
            "வங்கி கணக்கு புத்தகம்"
        ],
        "required_documents_hi": [
            "छात्र का आधार कार्ड (बैंक से लिंक)",
            "पिछली कक्षा की अंकसूची",
            "कॉलेज बोनाफाइड एवं फीस रसीद",
            "आय प्रमाण पत्र व जाति प्रमाण पत्र",
            "बैंक पासबुक"
        ],
        "required_documents_mr": [
            "आधार कार्ड, बँक पासबुक, मागील वर्षाचे गुणपत्रक, बोनाफाईड प्रमाणपत्र, उत्पन्न व जात दाखला"
        ],
        "required_documents_bn": [
            "আধার কার্ড, আগের ক্লাসের মার্কশিট, কলেজের ফি রসিদ, আয়ের সনদ ও ব্যাংক পাসবুক"
        ],
        "application_steps_en": [
            "Step 1: Register at scholarships.gov.in using Aadhaar number and mobile OTP.",
            "Step 2: Fill One-Time Registration (OTR) to obtain Reference ID.",
            "Step 3: Select appropriate Scheme (Pre-matric, Post-matric, MCM, State Scheme).",
            "Step 4: Upload Bonafide certificate, marksheet, and income certificate.",
            "Step 5: College/Institute verifies application online (Level 1).",
            "Step 6: District / State Nodal Officer approves; money credited directly via DBT."
        ],
        "application_steps_ta": [
            "படி 1: scholarships.gov.in தளத்தில் ஆதார் எண் கொண்டு ஒருமுறை பதிவு (OTR) செய்யவும்.",
            "படி 2: கல்வித் திட்டம் மற்றும் உதவித்தொகை வகையைத் தேர்வு செய்யவும்.",
            "படி 3: கல்லூரியில் Bonafide சான்று, மதிப்பெண் பட்டியல், வருமானச் சான்றை பதிவேற்றவும்.",
            "படி 4: கல்லூரி முதல்வர் இணையவழியில் சரிபார்த்து ஒப்புதல் அளிப்பார்.",
            "படி 5: மாவட்ட அலுவலர் ஒப்புதலுக்குப் பின் நேரடியாக வங்கி கணக்கில் தொகை வரவு வைக்கப்படும்."
        ],
        "application_steps_hi": [
            "चरण 1: scholarships.gov.in पर OTR पंजीकरण करें।",
            "चरण 2: उपयुक्त छात्रवृत्ति चुनें और दस्तावेज अपलोड करें।",
            "चरण 3: संस्थान (स्कूल/कॉलेज) द्वारा ऑनलाइन सत्यापन किया जाएगा।",
            "चरण 4: नोडल अधिकारी के अनुमोदन के बाद डीबीटी द्वारा राशि खाते में आएगी।"
        ],
        "application_steps_mr": [
            "पायरी 1: scholarships.gov.in वर OTR नोंदणी करा.",
            "पायरी 2: अर्ज भरून कागदपत्रे जोडा. कॉलेजच्या पडताळणीनंतर शिष्यवृत्ती थेट खात्यात जमा होते."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: scholarships.gov.in পোর্টালে OTR নিবন্ধন করুন।",
            "পদক্ষেপ ২: প্রতিষ্ঠান কর্তৃক ভেরিফিকেশনের পর সরাসরি ব্যাংক অ্যাকাউন্টে টাকা জমা হবে।"
        ],
        "fees_en": "100% Free of charge.",
        "processing_time_en": "Disbursement aligned with academic semester / financial year cycle."
    },
    {
        "id": "public_grievances",
        "name_en": "Government Grievances, Complaints & Delayed Applications",
        "name_ta": "அரசு குறைதீர்ப்பு, புகார் மற்றும் தாமதமான விண்ணப்பங்கள்",
        "name_hi": "सरकारी शिकायत निवारण, देरी व समस्या समाधान (CPGRAMS / 1100)",
        "name_mr": "शासकीय तक्रार निवारण व प्रलंबित अर्ज पाठपुरावा",
        "name_bn": "সরকারি অভিযোগ ও বিলম্বিত আবেদনের সমাধান (Public Grievance)",
        "category": "Citizen Services & Grievance Redressal",
        "government_level": "Central & State Governments (CPGRAMS / CM Helpline 1100)",
        "official_portal": "https://pgportal.gov.in/",
        "official_source_citation": "Department of Administrative Reforms and Public Grievances (DARPG) / Tamil Nadu CM Helpline (cmhelpline.tnega.org)",
        "keywords": [
            "complaint", "grievance", "cpgrams", "cm helpline", "1100", "delayed application",
            "rejected application", "file complaint", "helpline", "corruption", "inaction",
            "புகார்", "குறைதீர்ப்பு", "முதல்வர் உதவி மையம்", "மனு", "தாமதம்", "நிராகரிப்பு",
            "शिकायत", "समस्या", "सीएम हेल्पलाइन", "जनसुनवाई", "सीपीग्राम्स",
            "तक्रार", "तक्रार निवारण", "आपले सरकार तक्रार",
            "অভিযোগ", "অভিযোগ সমাধান", "সিপিগ্র্যামস", "দেরি"
        ],
        "benefit_en": "Centralized, time-bound grievance redressal mechanism. Citizens can lodge complaints against delayed government applications, officer inaction, denial of entitled benefits (pension, ration, electricity, water), or bribery, with mandatory officer action within 30 days.",
        "benefit_ta": "அரசு சேவைகளில் ஏற்படும் தேவையற்ற தாமதங்கள், ஓய்வூதியம் கிடைக்காதது, குடும்ப அட்டை மறுப்பு போன்ற பிரச்சனைகளுக்கு முதல்வர் உதவி எண் 1100 அல்லது CPGRAMS வழியாக நேரடியாக புகார் அளித்து 30 நாட்களுக்குள் தீர்வு காணலாம்.",
        "benefit_hi": "सरकारी सेवाओं में देरी, पेंशन या राशन न मिलने अथवा अधिकारियों द्वारा लापरवाही पर 30 दिनों में अनिवार्य समाधान हेतु आधिकारिक शिकायत निवारण प्रणाली।",
        "benefit_mr": "शासकीय कामांतील विलंब, योजनांचा लाभ न मिळणे याविरोधात थेट वरिष्ठ अधिकाऱ्यांकडे तक्रार करून ३० दिवसांत न्याय मिळवण्याची सुविधा.",
        "benefit_bn": "সরকারি পরিষেবা পেতে অযথা বিলম্ব বা অনিয়মের বিরুদ্ধে সরাসরি অভিযোগ জানানোর এবং ৩০ দিনে সমাধান পাওয়ার সরকারি ব্যবস্থা।",
        "eligibility_rules_en": [
            "Any Indian citizen can register a grievance against central or state government departments.",
            "Sub-judice matters (cases pending in court) or RTI appeals cannot be filed as grievances."
        ],
        "eligibility_rules_ta": [
            "எந்த இந்திய குடிமகனும் மத்திய மற்றும் மாநில அரசுத் துறைகளுக்கு எதிராக புகார் பதிவு செய்யலாம்.",
            "நீதிமன்றத்தில் நிலுவையில் உள்ள வழக்குகள் தவிர மற்ற அனைத்து சேவை குறைகளுக்கும் பொருந்தும்."
        ],
        "eligibility_rules_hi": [
            "कोई भी नागरिक शिकायत दर्ज करा सकता है। न्यायालयीन मामलों को छोड़कर।"
        ],
        "eligibility_rules_mr": [
            "कोणताही नागरिक सरकारी सेवेतील त्रुटींविरोधात तक्रार नोंदवू शकतो."
        ],
        "eligibility_rules_bn": [
            "যে কোনো নাগরিক সরকারি পরিষেবার গাফিলতির বিরুদ্ধে অভিযোগ জানাতে পারেন।"
        ],
        "required_documents_en": [
            "Previous Application Reference Number / Acknowledgement receipt (for delayed services)",
            "Aadhaar Number or Mobile Number of the citizen",
            "Copies of earlier letters or receipts submitted to the department"
        ],
        "required_documents_ta": [
            "தாமதமான விண்ணப்பத்தின் ஒப்புகைச் சீட்டு அல்லது குறிப்பு எண் (Reference Number)",
            "ஆதார் எண் மற்றும் தொடர்பு மொபைல் எண்",
            "முந்தைய மனுவின் நகல் (இருப்பின்)"
        ],
        "required_documents_hi": [
            "पुराना आवेदन संदर्भ क्रमांक (Reference Number)",
            "मोबाइल नंबर और आधार कार्ड"
        ],
        "required_documents_mr": [
            "अर्जाचा संदर्भ क्रमांक व मोबाईल नंबर"
        ],
        "required_documents_bn": [
            "পূর্ববর্তী আবেদনের রেফারেন্স নম্বর ও মোবাইল নম্বর"
        ],
        "application_steps_en": [
            "Option A (Tamil Nadu State Helpline): Dial toll-free 1100 from any phone, or visit cmhelpline.tnega.org to register grievance.",
            "Option B (Central Govt & National Services): Register at pgportal.gov.in (CPGRAMS) or use UMANG app.",
            "Step 3: Select Ministry/Department (e.g., Revenue, Banking, Social Welfare, Transport).",
            "Step 4: Describe issue, mention previous application number, and upload proof.",
            "Step 5: Track grievance resolution using the unique Grievance Registration Number.",
            "Step 6: If unsatisfied, file an appeal to the Appellate Authority directly on the portal."
        ],
        "application_steps_ta": [
            "முறை 1 (தமிழ்நாடு): எந்த போனில் இருந்தும் 1100 என்ற கட்டணமில்லா எண்ணை அழைத்து புகார் பதிவு செய்யவும், அல்லது cmhelpline.tnega.org தளத்தில் பதிவு செய்யவும்.",
            "முறை 2 (மத்திய அரசு/வங்கி/ரயில்வே): pgportal.gov.in (CPGRAMS) வழியே புகார் பதிவு செய்யவும்.",
            "படி 3: துறை மற்றும் பிரச்சனையை சுருக்கமாக எழுதி பழைய விண்ணப்ப எண்ணைக் குறிப்பிடவும்.",
            "படி 4: உங்களுக்கு ஒரு புகார் எண் (Grievance Number) SMS-இல் வரும்.",
            "படி 5: 30 நாட்களுக்குள் சம்பந்தப்பட்ட உயர் அதிகாரி விசாரணை செய்து நடவடிக்கை எடுப்பார்.",
            "படி 6: பதில் திருப்திகரமாக இல்லை என்றால் தளத்திலேயே மேல்முறையீடு (Appeal) செய்யலாம்."
        ],
        "application_steps_hi": [
            "विकल्प 1: राज्य हेल्पलाइन (जैसे 1100 या जनसुनवाई) पर कॉल या ऑनलाइन शिकायत दर्ज करें।",
            "विकल्प 2: केंद्र सरकार व राष्ट्रीय सेवाओं के लिए pgportal.gov.in (CPGRAMS) का उपयोग करें।",
            "चरण 3: विभाग चुनें, समस्या का विवरण दें और पिछला संदर्भ नंबर लिखें।",
            "चरण 4: एसएमएस पर प्राप्त शिकायत क्रमांक से स्थिति ट्रैक करें। 30 दिन में समाधान अनिवार्य है।"
        ],
        "application_steps_mr": [
            "पायरी 1: केंद्र शासनासाठी pgportal.gov.in किंवा राज्य हेल्पलाईनवर तक्रार नोंदवा.",
            "पायरी 2: तक्रार क्रमांक मिळवून ३० दिवसांच्या आत कारवाईची स्थिती तपासा."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: pgportal.gov.in (CPGRAMS) বা রাজ্য হেল্পলাইনে যোগাযোগ করুন।",
            "পদক্ষেপ ২: অভিযোগ নম্বর দিয়ে ৩০ দিনের মধ্যে সমাধান ট্র্যাক করুন।"
        ],
        "fees_en": "100% Free of cost. CM Helpline 1100 is toll-free.",
        "processing_time_en": "Mandated resolution within 30 days."
    },
    {
        "id": "record_corrections",
        "name_en": "Correction of Details in Government Records (Name, DOB, Address)",
        "name_ta": "அரசு ஆவணங்களில் திருத்தம் செய்தல் (பெயர், பிறந்த தேதி, முகவரி)",
        "name_hi": "सरकारी दस्तावेजों में सुधार (नाम, जन्म तिथि, पता)",
        "name_mr": "शासकीय कागदपत्रांमधील दुरुस्ती (नाव, जन्मतारीख, पत्ता)",
        "name_bn": "সরকারি তথ্যে সংশোধন (নাম, জন্মতারিখ, ঠিকানা)",
        "category": "Documentation Updates & Name Corrections",
        "government_level": "Central & State Departments",
        "official_portal": "https://www.india.gov.in/",
        "official_source_citation": "National Government Services Portal / UIDAI / ECI / NSDL",
        "keywords": [
            "correction", "correct name", "dob correction", "address update",
            "spelling mistake", "name change", "gazette", "wrong details",
            "திருத்தம்", "பெயர் மாற்றம்", "பிறந்த தேதி மாற்றம்", "தவறான விவரம்", "எழுத்துப்பிழை",
            "सुधार", "नाम सुधार", "जन्म तिथि सुधार", "पता बदलना", "त्रुटि",
            "दुरुस्ती", "नाव बदल", "पत्ता दुरुस्ती", "चूक",
            "সংশোধন", "নাম সংশোধন", "ভুল সংশোধন"
        ],
        "benefit_en": "Standardized official procedures to correct discrepancies in names, dates of birth, spelling mistakes, or residential addresses across Aadhaar, PAN, Voter ID, Ration Card, and School Certificates to ensure seamless access to pensions and government services.",
        "benefit_ta": "ஆதார், பான், வாக்காளர் அட்டை அல்லது ரேஷன் கார்டில் உள்ள பெயர் எழுத்துப்பிழை, பிறந்த தேதி மற்றும் முகவரியை அதிகாரப்பூர்வமாக திருத்துவதற்கான நடைமுறைகள். இதனால் ஓய்வூதியம் மற்றும் பிற சலுகைகள் தடங்கலின்றி கிடைக்கும்.",
        "benefit_hi": "आधार, पैन, वोटर आईडी या राशन कार्ड में गलत नाम, जन्म तिथि या पते को सुधारने की आधिकारिक प्रक्रिया।",
        "benefit_mr": "आधार, पॅन किंवा मतदार ओळखपत्रातील नावाची स्पेलिंग किंवा जन्मतारीख दुरुस्त करण्याची अधिकृत पद्धत.",
        "benefit_bn": "আধার, প্যান বা ভোটার কার্ডে ভুল নাম, জন্মতারিখ বা ঠিকানা সংশোধনের সরকারি পদ্ধতি।",
        "eligibility_rules_en": [
            "Any cardholder with valid supporting evidence (Birth Certificate, School TC, Gazette publication, or Marriage certificate).",
            "Aadhaar name change allowed up to 2 times; Date of birth change allowed only once in a lifetime."
        ],
        "eligibility_rules_ta": [
            "சரியான ஆதரவு ஆவணம் (பிறப்புச் சான்றிதழ், பள்ளி TC அல்லது அரசிதழ்) வைத்திருக்கும் எவரும் திருத்தம் செய்யலாம்.",
            "ஆதாரில் பெயர் மாற்றம் 2 முறை மட்டுமே அனுமதிக்கப்படும்; பிறந்த தேதி வாழ்நாளில் 1 முறை மட்டுமே திருத்த முடியும்."
        ],
        "eligibility_rules_hi": [
            "वैध प्रमाण (जन्म प्रमाण पत्र, स्कूल टीसी) उपलब्ध होना चाहिए।",
            "आधार में नाम 2 बार और जन्म तिथि जीवन में केवल 1 बार बदली जा सकती है।"
        ],
        "eligibility_rules_mr": [
            "पुरावा म्हणून जन्म दाखला किंवा शाळा सोडल्याचा दाखला आवश्यक."
        ],
        "eligibility_rules_bn": [
            "সঠিক প্রমাণপত্র (জন্ম সনদ বা স্কুল সার্টিফিকেট) থাকলে সংশোধন সম্ভব।"
        ],
        "required_documents_en": [
            "For Name Correction: Birth Certificate, Passport, School Marksheet, or State Gazette notification",
            "For DOB Correction: Birth Certificate issued by Municipal Authority",
            "For Address Update: Electricity/Water bill, Ration card, Bank statement, or Rent agreement",
            "For Marital Name Change: Marriage Certificate or Joint Photograph Affidavit"
        ],
        "required_documents_ta": [
            "பெயர் திருத்தத்திற்கு: பிறப்புச் சான்றிதழ், பள்ளி சான்றிதழ் அல்லது அரசு அரசிதழ் (Gazette)",
            "பிறந்த தேதி திருத்தத்திற்கு: நகராட்சி வழங்கிய அசல் பிறப்புச் சான்றிதழ் கட்டாயம்",
            "முகவரி திருத்தத்திற்கு: மின்சார மசோதா, குடும்ப அட்டை, அல்லது வங்கி கணக்கு புத்தகம்"
        ],
        "required_documents_hi": [
            "नाम सुधार हेतु: जन्म प्रमाण पत्र, स्कूल अंकपत्र या गजट अधिसूचना",
            "जन्म तिथि सुधार हेतु: जन्म प्रमाण पत्र",
            "पता सुधार हेतु: बिजली बिल, राशन कार्ड, बैंक पासबुक"
        ],
        "required_documents_mr": [
            "नाव दुरुस्तीसाठी: जन्म दाखला किंवा गॅझेट",
            "जन्मतारखेसाठी: अधिकृत जन्म दाखला"
        ],
        "required_documents_bn": [
            "নাম সংশোধনের জন্য: জন্ম সনদ বা গ্যাজেট নোটিফিকেশন"
        ],
        "application_steps_en": [
            "Aadhaar Correction: Update address online at myaadhaar.uidai.gov.in. For Name/DOB/Biometrics, visit Aadhaar Seva Kendra in person.",
            "PAN Card Correction: Apply online via Form 'Changes or Correction in PAN Data' at Protean (NSDL) / UTIITSL with supporting ID.",
            "Voter ID Correction: Submit Form 8 online at voters.eci.gov.in with correct proofs.",
            "Ration Card Correction: Edit member details, spelling, or address at tnpds.gov.in.",
            "Legal Full Name Change: Publish notification in State Official Gazette (Stationery & Printing Dept)."
        ],
        "application_steps_ta": [
            "ஆதார் திருத்தம்: முகவரியை myaadhaar.uidai.gov.in இல் ஆன்லைனில் மாற்றலாம். பெயர் மற்றும் பிறந்த தேதிக்கு ஆதார் சேவை மையத்திற்கு நேரில் செல்ல வேண்டும்.",
            "பான் கார்டு திருத்தம்: NSDL / UTIITSL தளத்தில் 'Changes in PAN' விண்ணப்பம் வழியே ஆன்லைனில் திருத்தலாம்.",
            "வாக்காளர் அட்டை திருத்தம்: voters.eci.gov.in தளத்தில் படிவம் 8 (Form 8) மூலம் பெயர், வயது அல்லது முகவரியை திருத்தலாம்.",
            "ரேஷன் கார்டு திருத்தம்: tnpds.gov.in இல் குடும்ப அட்டை உறுப்பினர் பெயர் அல்லது முகவரியை மாற்றலாம்.",
            "முழு பெயர் மாற்றம் செய்ய: தமிழ்நாடு அரசு அரசிதழில் (Gazette) விண்ணப்பித்து விளம்பரம் செய்ய வேண்டும்."
        ],
        "application_steps_hi": [
            "आधार सुधार: पता myaadhaar पर ऑनलाइन बदलें; नाम व जन्म तिथि के लिए आधार केंद्र जाएं।",
            "पैन कार्ड सुधार: NSDL पोर्टल पर 'Correction in PAN' फॉर्म भरें।",
            "वोटर कार्ड सुधार: voters.eci.gov.in पर फॉर्म 8 ऑनलाइन भरें।",
            "राशन कार्ड सुधार: राज्य खाद्य पोर्टल पर संशोधन करें।"
        ],
        "application_steps_mr": [
            "आधार: पत्ता ऑनलाइन बदला; नावासाठी आधार केंद्रात जा.",
            "पॅन: NSDL वर Correction फॉर्म भरा.",
            "मतदार ओळखपत्र: voters.eci.gov.in वर फॉर्म ८ भरा."
        ],
        "application_steps_bn": [
            "আধার: ঠিকানা অনলাইনে বদলান; নাম বা বয়সের জন্য আধার কেন্দ্রে যান।",
            "প্যান: NSDL-এ Correction ফর্ম পূরণ করুন।",
            "ভোটার আইডি: ফর্ম ৮ পূরণ করুন।"
        ],
        "fees_en": "Aadhaar demographic: ₹50. PAN correction: ₹107. Voter ID correction: Free. Gazette publication: ₹500–₹1,000.",
        "processing_time_en": "10–25 working days across respective departments."
    },
    {
        "id": "ayushman_bharat_pmjay",
        "name_en": "Ayushman Bharat PMJAY (Pradhan Mantri Jan Arogya Yojana)",
        "name_ta": "ஆயுஷ்மான் பாரத் PM-JAY மருத்துவக் காப்பீடு",
        "name_hi": "आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना (PM-JAY)",
        "name_mr": "आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना (PM-JAY)",
        "name_bn": "আয়ুষ্মান ভারত প্রধানমন্ত্রী জন আরোগ্য যোজনা (PM-JAY)",
        "category": "Healthcare & Medical Cover",
        "government_level": "Central Government (National Health Authority)",
        "official_portal": "https://pmjay.gov.in/",
        "official_source_citation": "National Health Authority, Ministry of Health & Family Welfare",
        "keywords": [
            "ayushman bharat", "pmjay", "pm jan arogya", "golden card", "health card",
            "ayushman card", "central health scheme", "5 lakh insurance", "health cover",
            "ஆயுஷ்மான்", "ஆயுஷ்மான் பாரத்", "மருத்துவக் காப்பீடு", "கோல்டன் கார்டு",
            "आयुष्मान", "आयुष्मान भारत", "स्वास्थ्य बीमा", "गोल्डन कार्ड", "5 लाख",
            "आयुष्मान भारत", "आरोग्य विमा", "गोल्डन कार्ड",
            "আয়ুষ্মান ভারত", "স্বাস্থ্য বীমা", "গোল্ডেন কার্ড", "৫ লাখ"
        ],
        "benefit_en": "Cashless health cover up to ₹5 lakh per family per year for secondary and tertiary care hospitalization across empanelled public and private hospitals in India. Covers surgeries, medicines, and diagnostic tests without out-of-pocket costs.",
        "benefit_ta": "குடும்பத்திற்கு ஆண்டுக்கு ₹5 லட்சம் வரை அங்கீகரிக்கப்பட்ட அரசு மற்றும் தனியார் மருத்துவமனைகளில் இலவச கட்டணமில்லா சிகிச்சை. அறுவை சிகிச்சை, மருந்துகள் மற்றும் பரிசோதனைகள் இலவசம்.",
        "benefit_hi": "देश भर के सूचीबद्ध अस्पतालों में प्रति परिवार प्रति वर्ष 5 लाख रुपये तक का कैशलेस स्वास्थ्य उपचार। सर्जरी, दवाएं और जांचें निःशुल्क।",
        "benefit_mr": "प्रति कुटुंब दरवर्षी ५ लाख रुपयांपर्यंत मोफत कॅशलेस वैद्यकीय उपचार.",
        "benefit_bn": "প্রতি পরিবারকে বছরে ৫ লাখ টাকা পর্যন্ত বিনামূল্যে ক্যাশলেস চিকিৎসার সুবিধা।",
        "eligibility_rules_en": [
            "Families identified under Socio-Economic Caste Census (SECC 2011) and eligible deprivation criteria.",
            "Rural households with defined deprivation categories (kutcha house, female-headed, landless manual labour).",
            "Urban households in 11 defined occupational worker categories (domestic workers, street vendors, transport workers).",
            "Senior citizens aged 70 and above receive additional top-up cover."
        ],
        "eligibility_rules_ta": [
            "SECC 2011 சமூக பொருளாதார சாதி கணக்கெடுப்பில் பட்டியலிடப்பட்ட குடும்பங்கள்.",
            "கிராமப்புற மற்றும் நகர்ப்புற ஏழை, நலிவடைந்த தொழிலாளர் குடும்பங்கள்.",
            "70 வயது மற்றும் அதற்கு மேற்பட்ட மூத்த குடிமக்களுக்கு கூடுதல் சிறப்பு காப்பீடு."
        ],
        "eligibility_rules_hi": [
            "सामाजिक-आर्थिक जाति जनगणना (SECC 2011) के अंतर्गत सूचीबद्ध पात्र परिवार।",
            "ग्रामीण एवं शहरी क्षेत्रों के निर्धन व असंगठित क्षेत्र के श्रमिक परिवार।",
            "70 वर्ष और उससे अधिक आयु के वरिष्ठ नागरिकों के लिए विशेष अतिरिक्त स्वास्थ्य कवर।"
        ],
        "eligibility_rules_mr": [
            "SECC २०११ नुसार सामाजिक व आर्थिकदृष्ट्या दुर्बल वंचित कुटुंबे.",
            "ग्रामीण आणि शहरी भागातील गरीब व असंघटित कामगार कुटुंबे.",
            "७० वर्षे आणि त्यावरील ज्येष्ठ नागरिकांसाठी अतिरिक्त विमा संरक्षण."
        ],
        "eligibility_rules_bn": [
            "SECC ২০১১ জনগণনা অনুযায়ী চিহ্নিত সুবিধাবঞ্চিত পরিবার।",
            "গ্রামীণ ও শহুরে দরিদ্র ও অসংগঠিত শ্রমিক পরিবার।",
            "৭০ বছর বা তার বেশি বয়সী প্রবীণ নাগরিকদের জন্য অতিরিক্ত স্বাস্থ্য সুরক্ষা।"
        ],
        "required_documents_en": [
            "Aadhaar Card of all family members",
            "Ration Card or proof of family composition",
            "Mobile number linked with Aadhaar"
        ],
        "required_documents_ta": [
            "குடும்ப உறுப்பினர்கள் அனைவரின் ஆதார் அட்டை",
            "குடும்ப அட்டை (ரேஷன் கார்டு)",
            "ஆதாருடன் இணைக்கப்பட்ட மொபைல் எண்"
        ],
        "required_documents_hi": [
            "परिवार के सभी सदस्यों का आधार कार्ड",
            "राशन कार्ड या परिवार पहचान प्रमाण",
            "आधार से जुड़ा हुआ मोबाइल नंबर"
        ],
        "required_documents_mr": [
            "सर्व कुटुंब सदस्यांचे आधार कार्ड",
            "रेशन कार्ड किंवा कुटुंब नोंद पुरावा",
            "आधारशी जोडलेला मोबाईल क्रमांक"
        ],
        "required_documents_bn": [
            "পরিবারের সকল সদস্যের আধার কার্ড",
            "রেশন কার্ড বা পারিবারিক নথি",
            "আধারের সাথে যুক্ত মোবাইল নম্বর"
        ],
        "application_steps_en": [
            "Step 1: Check eligibility at beneficiary.nha.gov.in or nearest CSC/e-Seva or empanelled hospital.",
            "Step 2: Complete e-KYC using Aadhaar OTP, iris, or fingerprint.",
            "Step 3: Download and print Ayushman Golden Card.",
            "Step 4: Present Ayushman Card at Ayushman Mitra desk in empanelled hospital for cashless treatment."
        ],
        "application_steps_ta": [
            "படி 1: beneficiary.nha.gov.in அல்லது பொது சேவை மையத்தில் (CSC) தகுதி சரிபார்க்கவும்.",
            "படி 2: ஆதார் பயோமெட்ரிக் அல்லது OTP மூலம் e-KYC சரிபார்ப்பை முடிக்கவும்.",
            "படி 3: ஆயுஷ்மான் கோல்டன் கார்டை பதிவிறக்கம் செய்து அச்சிடவும்.",
            "படி 4: சிகிச்சை பெற மருத்துவமனையில் ஆயுஷ்மான் மித்ராவிடம் அட்டை காண்பிக்கவும்."
        ],
        "application_steps_hi": [
            "चरण 1: beneficiary.nha.gov.in या निकटतम सीएससी (CSC) या अस्पताल में अपनी पात्रता जांचें।",
            "चरण 2: आधार ओटीपी या बायोमेट्रिक द्वारा ई-केवाईसी पूर्ण करें।",
            "चरण 3: आयुष्मान गोल्डन कार्ड डाउनलोड और प्रिंट करें।",
            "चरण 4: कैशलेस उपचार हेतु सूचीबद्ध अस्पताल के आयुष्मान मित्र काउंटर पर कार्ड प्रस्तुत करें।"
        ],
        "application_steps_mr": [
            "पायरी १: beneficiary.nha.gov.in किंवा सीएससी (CSC) केंद्रावर पात्रता तपासा.",
            "पायरी २: आधार बायोमेट्रिक किंवा ओटीपी द्वारे e-KYC पूर्ण करा.",
            "पायरी ३: आयुष्यमान गोल्डन कार्ड डाउनलोड व प्रिंट करा.",
            "पायरी ४: कॅशलेस उपचारासाठी सूचीबद्ध रुग्णालयातील आयुष्यमान मित्र कक्षात कार्ड सादर करा."
        ],
        "application_steps_bn": [
            "পদক্ষেপ ১: beneficiary.nha.gov.in অথবা সিএসসি (CSC) কেন্দ্রে গিয়ে যোগ্যতা যাচাই করুন।",
            "পদক্ষেপ ২: আধার বায়োমেট্রিক বা ওটিপির মাধ্যমে e-KYC সম্পন্ন করুন।",
            "পদক্ষেপ ৩: আয়ুষ্মান গোল্ডেন কার্ড ডাউনলোড ও প্রিন্ট করুন।",
            "পদক্ষেপ ৪: তালিকাভুক্ত হাসপাতালে ক্যাশলেস চিকিৎসার জন্য আয়ুষ্মান মিত্র কাউন্টারে কার্ড দেখান।"
        ],
        "fees_en": "Free of cost. No registration or treatment charges for beneficiaries.",
        "fees_ta": "இலவசம். பயனாளிகளுக்கு பதிவு மற்றும் சிகிச்சைக் கட்டணம் எதுவும் இல்லை.",
        "fees_hi": "पूर्णतः निःशुल्क। पात्र लाभार्थियों से कोई पंजीकरण या उपचार शुल्क नहीं लिया जाता।",
        "fees_mr": "पूर्णपणे मोफत. नोंदणी किंवा उपचारासाठी कोणतेही शुल्क नाही.",
        "fees_bn": "সম্পূর্ণ বিনামূল্যে। সুবিধাভোগীদের জন্য কোনো নিবন্ধন বা চিকিৎসা ফি নেই।",
        "processing_time_en": "Instant Golden Card generation upon Aadhaar verification. Immediate cashless treatment approval at hospitals.",
        "processing_time_ta": "ஆதார் சரிபார்ப்புக்குப் பின் உடனடியாக கோல்டன் கார்டு. மருத்துவமனையில் உடனடி சிகிச்சை அனுமதி.",
        "processing_time_hi": "आधार सत्यापन पर तत्काल गोल्डन कार्ड जारी। अस्पताल में तत्काल कैशलेस स्वीकृति।",
        "processing_time_mr": "आधार पडताळणीनंतर त्वरित गोल्डन कार्ड उपलब्ध. रुग्णालयात त्वरित कॅशलेस मंजुरी.",
        "processing_time_bn": "আধার যাচাইকরণের সাথে সাথে গোল্ডেন কার্ড তৈরি। হাসপাতালে অবিলম্বে ক্যাশলেস অনুমোদন।"
    }
]
