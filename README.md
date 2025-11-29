# 📄 Annual Report Summarizer – AI Powered (LLMs + Vector Search + Streamlit)

Transform long and complex corporate annual reports into **clean, structured, AI-generated summaries** with multilingual translation, audio generation, and PDF export features.

---

<div align="center">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/Llama-3.3%2070B-Groq-000000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/VectorDB-ChromaDB-3CB371?style=for-the-badge" />
</div>

---

## 🚀 Project Overview

Annual Report Summarizer is an **AI-powered Streamlit application** that processes annual report PDFs and generates **high-quality summaries** for major sections such as:

- Business Information  
- Corporate Information  
- Chairman’s Letter  
- Board’s Report  
- Shareholding Pattern  
- Corporate Governance  
- MD&A  
- Consolidated Financial Statements  

The app uses:

- **Google Gemini 2.5 Flash** for summarization  
- **Groq Llama-3.3-70B** for multi-query deep retrieval  
- **ChromaDB + BGE embeddings** for semantic search  
- **Deep Translator** for multilingual translation  
- **gTTS** for audio narration  
- **pdfkit + wkhtmltopdf** for PDF export  

---

## 🌟 Features

### 🔹 AI Summaries  
Auto-generates structured summaries for 8 mandatory annual report sections.

### 🔹 Multi-Query Retrieval  
Enhances context recall using Llama-3.3-70B powered query expansion.

### 🔹 Translation Support  
Translate entire summary output into **15+ languages**.

### 🔹 Audio Generation  
Download narrated summaries in **MP3 format**.

### 🔹 PDF Export  
Download summaries as clean PDF files.

### 🔹 Secure Login  
Built-in authentication system (username + password hashing).

---

## 🧠 Tech Stack

| Category | Technology |
|---------|------------|
| Framework | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| Query Generator | Groq Llama-3.3-70B |
| Vector DB | ChromaDB |
| Embeddings | BAAI/bge-base-en-v1.5 |
| Text Extraction | PyMuPDF |
| TTS | gTTS |
| Translation | Deep Translator |
| PDF Engine | pdfkit (wkhtmltopdf) |
| Auth | Custom Python Auth |

---

## 📂 Project Structure

  📦 Annual-Report-Summarizer
  │
  ├── app.py # Main Streamlit application
  ├── auth.py # Login system
  ├── audio.py # Text-to-speech (MP3 generation)
  ├── translate.py # Language translation logic
  ├── pdf_processing.py # PDF extraction, cleaning, chunking
  ├── summarizer.py # LLM summarization logic
  ├── vectorstore.py # ChromaDB vector store creation
  ├── prompts.py # Section-level retrieval & summary prompts
  ├── requirements.txt # Dependencies
  ├── check.py # wkhtmltopdf setup test script
  └── assets/ # Images, logos

