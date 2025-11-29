# 📄 Annual Report Summarizer – AI Powered (LLMs + Vector Search + Streamlit)

Transform long and complex corporate annual reports into **clean, structured, AI-generated summaries** with multilingual translation, audio generation, and PDF export features.

---

<div align="center">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" />
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


# ⚙️ Setup Guide

Follow the steps below to install and run the **Annual Report Summarizer** on your local system.

---
1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>


2️⃣ Create Virtual Environment Windows
      python -m venv venv
      venv\Scripts\activate

Mac / Linux
      python3 -m venv venv
      source venv/bin/activate

3️⃣ Install Dependencies
      pip install -r requirements.txt

4️⃣ Install wkhtmltopdf (Required for PDF Export)

      Download from:
      👉 https://wkhtmltopdf.org/downloads.html
      
      Verify installation:
      
      python check.py


If everything is correct, you'll see a successful PDF generation message.

5️⃣ Create .env File

      Create a new file named .env in the project root and add the following:
      
      GOOGLE_API_KEY=your_google_api_key
      GROQ_API_KEY=your_groq_api_key
      APP_USERNAME=admin
      APP_PASSWORD=1234

🔑 Get API Keys

      Google Gemini API Key: https://aistudio.google.com
      
      Groq API Key: https://console.groq.com/keys

6️⃣ Run the Application
      streamlit run app.py


Open the app in your browser:
👉 http://localhost:8501/

7️⃣ Login

      Use the credentials (or your own if changed in .env):
      
      Username: admin
      Password: 1234

🎉 You're Ready!

Upload any annual report PDF and start generating:

      AI Summaries
      
      Translations
      
      Audio Narration
      
      Downloadable PDFs

Enjoy using the AI-powered Annual Report Summarizer 🚀
 

