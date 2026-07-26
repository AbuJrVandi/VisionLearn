# VisionLearn

**AI-Powered Assistive Learning Platform for Visually Impaired Students**

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=white)](https://reactjs.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?style=flat&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

VisionLearn is a web-based assistive learning platform purpose-built for **visually impaired students at the Milton Margai School for the Blind** in Sierra Leone. It implements the five-layer AI system architecture proposed in our research thesis, combining speech interaction, OCR, text-to-speech, and an intelligent AI tutor to make educational content accessible to all.

---

## Features

### 🎙️ Voice Assistant
Ask questions using your voice and receive spoken answers. The assistant uses browser speech recognition, backend AI processing, and natural-sounding neural TTS (Microsoft Edge) for a fully hands-free experience.

### 📄 Smart Document Scanner
Photograph or upload textbook pages, notes, or worksheets. The system applies multi-strategy OCR preprocessing (adaptive thresholding, sharpening, Otsu, inversion) and multi-PSM fallback to extract text accurately from low-quality images.

### 🤖 AI Chat Tutor
Get detailed, curriculum-aligned explanations across five subjects — Mathematics, Science, English, Social Studies, and Vocational Studies. The tutor checks an extensive offline knowledge base first, then falls back to AI APIs (Gemini / Pollinations) when needed.

### 📚 Document Library
Upload, organise, search, and listen to learning materials. Supports PDF, DOCX, TXT, Markdown, and scanned documents. Each document is automatically categorised by subject.

### 📊 Learning Analytics
Track study activity, chat history, document usage, and daily/hourly learning patterns through interactive charts.

### ♿ Accessibility First
- Screen reader optimised with ARIA labels throughout
- Keyboard-navigable interface
- High contrast mode toggle
- Four adjustable font size levels
- Voice-based input and output
- Skip-to-content navigation

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Vercel)                            │
│        React 18 + Tailwind CSS + Recharts + Lucide Icons        │
│        Voice Interaction · Document Viewer · Analytics          │
├─────────────────────────────────────────────────────────────────┤
│                         REST API (/api/*)                       │
├─────────────────────────────────────────────────────────────────┤
│                     Backend (Render / Local)                    │
│    FastAPI · SQLite (aiosqlite) · Gunicorn + Uvicorn Workers   │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│   OCR    │   TTS    │   STT    │  Chat    │  Knowledge Base    │
│Tesseract │Edge TTS  │Web Speech│Gemini /  │400+ curriculum     │
│Multi-    │AriaNeural│API +     │Pollina-  │entries across 5    │
│strategy  │voice     │fallback  │tions /   │subjects (offline   │
│preproces-│(no SSML) │          │Offline   │fallback)           │
│sing      │          │          │Knowledge │                    │
└──────────┴──────────┴──────────┴──────────┴────────────────────┘
```

**Data Flow:**
1. User speaks or types a question → Frontend sends to `/api/chat/send`
2. Backend checks offline Knowledge Base first (instant, no API needed)
3. If no match → tries Pollinations.ai → Gemini API in sequence
4. Response returned → Frontend displays text + plays via neural TTS

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, React Router 6, Tailwind CSS 3, Recharts, Lucide React |
| **Backend** | FastAPI, Uvicorn, Gunicorn, SQLite, aiosqlite |
| **OCR** | Tesseract 5 (pytesseract) with Pillow preprocessing |
| **TTS** | edge-tts (Microsoft Edge neural voice, en-US-AriaNeural) |
| **AI Chat** | Google Gemini 2.0 Flash, Pollinations.ai, offline knowledge base |
| **PDF** | PyMuPDF (fitz), python-docx |
| **Deployment** | Vercel (frontend), Render (backend) |

---

## Local Development

### Prerequisites

- **Python 3.11+** (3.13 recommended)
- **Node.js 18+**
- **Tesseract OCR** — `brew install tesseract` (macOS) or `apt install tesseract-ocr` (Linux)

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env to add API keys (optional — offline mode works without them)
uvicorn main:app --reload --port 8000
```

The backend runs at **http://localhost:8000**.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at **http://localhost:5173** and proxies `/api/*` to the backend.

---

## Deployment

### One-Click Deploy

| Platform | Service | Config |
|----------|---------|--------|
| [![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white)](https://vercel.com) | Frontend | Import `frontend/` directory. Set env `VITE_API_URL` to your Render URL. |
| [![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com) | Backend | Import repo with root dir `backend/`. Uses `render.yaml` for auto-config. |

**Environment Variables (Render):**

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | No | Google Gemini API key (free at aistudio.google.com) |
| `GEMINI_MODEL` | No | Default: `gemini-2.0-flash` |
| `HF_API_KEY` | No | Hugging Face API token |
| `HF_MODEL` | No | Default: `mistralai/Mistral-7B-Instruct-v0.3` |
| `DEBUG` | No | Set `false` for production |

**Environment Variables (Vercel):**

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Full URL of your Render backend, e.g. `https://visionlearn-backend.onrender.com` |

> **No API key is required.** Without keys, the chat system uses the built-in offline educational knowledge base (400+ curriculum-aligned entries). Adding a Gemini or Hugging Face key enables richer AI-powered responses.

---

## Project Structure

```
VisionLearn/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Settings via pydantic-settings
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Local environment variables
│   ├── models/
│   │   └── database.py            # SQLite database setup
│   ├── routers/
│   │   ├── chat_routes.py         # Chat, sessions, analytics endpoints
│   │   ├── document_routes.py     # Upload, OCR, document management
│   │   └── voice_routes.py        # TTS and STT endpoints
│   └── services/
│       ├── chat_service.py        # AI provider chain + knowledge base
│       ├── knowledge_base.py      # Offline curriculum (400+ entries)
│       ├── ocr_service.py         # Multi-strategy OCR pipeline
│       ├── document_extraction.py # PDF/DOCX text extraction
│       ├── tts_service.py         # edge-tts speech synthesis
│       └── stt_service.py         # Speech-to-text transcription
├── frontend/
│   ├── src/
│   │   ├── pages/                 # Route pages (VoiceAssistant, Scanner, etc.)
│   │   ├── components/            # Reusable UI components
│   │   ├── hooks/                 # Custom React hooks (speech, etc.)
│   │   └── services/api.js        # API client with env-based URL
│   ├── vercel.json                # Vercel deployment configuration
│   └── package.json
├── render.yaml                    # Render blueprint configuration
└── README.md
```

---

## Academic Context

VisionLearn is part of a research thesis project at the Milton Margai School for the Blind in Sierra Leone. The platform implements a **five-layer AI system architecture** designed to address the unique accessibility challenges faced by visually impaired students in developing regions:

1. **Input Layer** — Voice, keyboard, document upload
2. **Processing Layer** — OCR, STT, NLP
3. **Knowledge Layer** — Offline curriculum + AI APIs
4. **Output Layer** — TTS, visual display, accessible UI
5. **Analytics Layer** — Usage tracking, progress monitoring

---

## License

Academic research project — Milton Margai School for the Blind, Sierra Leone.
