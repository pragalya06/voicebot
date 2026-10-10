# SevaMitra: AI-Powered Multilingual Government Service Assistant

An accessible, voice-first multilingual web application designed for rural citizens in India to discover, verify, and apply for government schemes in their mother tongue with **automatic spoken language detection**, OCR document checks, RAG-grounded official answers, and step-by-step application guidance.

---

## 🌟 Key Features

1. **Automatic Spoken Language Detection**:
   - Speak in **Tamil, English, Hindi, Marathi, or Bengali** without pre-selecting a language.
   - The system automatically detects the spoken language, adapts the website headings, menus, and buttons to that language, formulates verified answers in that language, and reads them aloud.
2. **AI Multilingual Assistant (RAG with LangChain & FAISS)**:
   - Grounded Q&A for flagship Central & State schemes (Old Age Pension, PM-KISAN, Kalaignar Magalir Urimai Thogai, CMCHIS Health Insurance, Destitute Widow Pension).
   - Zero hallucination: official citations, gazette links, and tailored audio summaries.
3. **Personalized Scheme Finder**:
   - Rural citizen interview (age, occupation, income ceiling) calculating eligibility match scores with transparent explanations.
4. **Document Readiness Checker (Tesseract OCR)**:
   - Scan or test Aadhaar cards, Income Certificates, Ration Cards, and Land Records (Patta/Chitta).
   - Automatic 12-digit Aadhaar number privacy masking (`XXXX-XXXX-8831`).
   - 1-click test sample documents for instant verification without physical papers.
5. **Step-by-Step Application Roadmap & Saved Checklist**:
   - Visual 4-to-5 stage journey from VAO certificate to e-Seva submission, RI verification, Tahsildar approval, and DBT monthly credit.
   - Persistent checklist saved to `localStorage`.
   - Application status tracker with 1-click demo reference numbers.

---

## 🇮🇳 Supported Languages

| Language | Native Label | Code | Speech Locale |
| :--- | :--- | :--- | :--- |
| **Tamil** | தமிழ் | `ta` | `ta-IN` |
| **Hindi** | हिन्दी | `hi` | `hi-IN` |
| **Marathi** | मराठी | `mr` | `mr-IN` |
| **Bengali** | বাংলা | `bn` | `bn-IN` |
| **English** | English | `en` | `en-IN` |

---

## 🚀 Local Development Setup

### 1. Backend Setup (FastAPI)
```powershell
cd backend
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install dependencies:
pip install -r requirements.txt

# Start backend server:
uvicorn app.main:app --reload --port 8000
```
- API Health Check: `http://localhost:8000/api/health`
- Swagger Documentation: `http://localhost:8000/docs`

### 2. Frontend Setup (React + Vite)
```powershell
cd frontend
npm install
npm run dev
```
- Frontend application accessible at: `http://localhost:5173`

### 3. Run Automated Tests
```powershell
cd backend
.\venv\Scripts\python.exe tests\test_language_detection.py
.\venv\Scripts\python.exe tests\test_multilingual_integration.py
.\venv\Scripts\python.exe tests\test_documents.py
.\venv\Scripts\python.exe tests\test_guidance.py
```

---

## ☁️ Cloud Deployment Guide

### Backend on Render (Web Service)
1. Link your GitHub repository to [Render](https://render.com).
2. Create a new **Web Service**:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Or use the included `render.yaml` blueprint.

### Frontend on Vercel
1. Link the repository to [Vercel](https://vercel.com).
2. Set root directory to `frontend`.
3. The included `vercel.json` automatically configures SPA routing and `/api/*` proxy rewrites to your backend Render URL.
