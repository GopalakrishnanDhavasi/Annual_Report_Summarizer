# app.py — Final Version (No PDF download for translated summaries)
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import streamlit as st
import pdfkit  # ✅ For PDF generation using wkhtmltopdf

# ✅ wkhtmltopdf path configuration (verified earlier)
PDFKIT_CONFIG = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

# Optional dotenv
try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except Exception:
    load_dotenv = lambda *a, **k: None
    _DOTENV_AVAILABLE = False

from auth import login, logout, login_ui
from prompts import section_summary_prompts
from pdf_processing import extract_text_from_pdf, preprocess_for_llm, chunk_document
from vectorstore import create_vector_store
from summarizer import summarize_all_sections

# Translation & Audio modules
try:
    import translate as translate_module
    _TRANSLATE_MODULE_AVAILABLE = True
except Exception:
    translate_module = None
    _TRANSLATE_MODULE_AVAILABLE = False

try:
    import audio as audio_module
    _AUDIO_MODULE_AVAILABLE = True
except Exception:
    audio_module = None
    _AUDIO_MODULE_AVAILABLE = False

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============ CONFIGURE LLM MODELS ============
def configure_genai():
    """Configure Gemini and Groq LLMs."""
    import google.generativeai as genai
    from langchain_groq import ChatGroq

    genai.configure(api_key=GOOGLE_API_KEY)
    llm_model = genai.GenerativeModel("gemini-2.5-flash")
    query_gen_llm = ChatGroq(
        temperature=0,
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile"
    )
    return llm_model, query_gen_llm


# ============ PDF CREATION FUNCTION ============
def create_pdf_pdfkit(summaries: dict, title: str = "Summaries") -> bytes:
    """
    Generate a clean, standard PDF using pdfkit (wkhtmltopdf backend).
    No Unicode fonts or local file dependencies.
    Safe for Windows systems without font setup.
    """

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, Helvetica, sans-serif;
                padding: 30px;
                background-color: #ffffff;
            }}
            h1 {{
                text-align: center;
                color: #2C3E50;
                margin-bottom: 25px;
            }}
            h2 {{
                color: #1A5276;
                margin-top: 25px;
            }}
            p {{
                font-size: 14px;
                line-height: 1.6;
                text-align: justify;
                color: #2c3e50;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
    """

    # Add sections and summaries
    for section, text in summaries.items():
        html += f"<h2>{section}</h2><p>{text}</p>"

    html += "</body></html>"

    # Generate the PDF safely (no file:// URLs)
    pdf_bytes = pdfkit.from_string(html, False, configuration=PDFKIT_CONFIG)
    return pdf_bytes



# ============ STREAMLIT PAGE SETUP ============
st.set_page_config(page_title="📊 Annual Report Summarizer", layout="wide")

# --- LOGIN HANDLER ---
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    left_col, right_col = st.columns([2, 1])
    with left_col:
        try:
            st.image("assets/ARSlogo.png", width=500)
        except Exception:
            st.markdown(
                """
                <div style='background:#f6f8fa; padding:32px; border-radius:12px;'>
                    <h1 style='margin:0; font-size:34px;'>Welcome back!</h1>
                    <p style='color:#6b7280; font-size:16px;'>Start managing your finance faster and better</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with right_col:
        st.markdown(
            "<div style='padding:18px; border-radius:10px; box-shadow:0 4px 14px rgba(0,0,0,0.06); background:white'>",
            unsafe_allow_html=True,
        )
        logged_in = login_ui(container=right_col)
        st.markdown("</div>", unsafe_allow_html=True)
        if not logged_in:
            st.stop()

# --- MAIN PAGE ---
st.title("📄 AI-Powered Annual Report Summarizer")
st.write("Upload an annual report PDF and get concise, AI-generated section summaries.")

# --- TERMS AND CONDITIONS ---
try:
    with open("TERMS.md", "r", encoding="utf-8") as tf:
        terms_text = tf.read()
except Exception:
    terms_text = "Terms and conditions are not available."

if not st.session_state.get("authenticated", False):
    st.stop()

st.sidebar.title("User Menu")
st.sidebar.markdown("<div style='height:60vh'></div>", unsafe_allow_html=True)
if st.sidebar.button("Logout"):
    logout()

if not st.session_state.get("accepted_terms", False):
    st.markdown("# Terms and Conditions")
    st.markdown(
        f"<div style='max-height:560px; overflow:auto; border:1px solid #e6e9ee; padding:18px; border-radius:8px'>{terms_text}</div>",
        unsafe_allow_html=True,
    )
    st.write("")
    agree_col1, agree_col2, agree_col3 = st.columns([1, 2, 1])
    with agree_col2:
        confirm = st.checkbox(
            "I confirm I have read and accept the Terms and that the uploaded PDF contains the sections listed above",
            key="accept_terms_confirm",
        )
        if st.button("Agree and Continue"):
            if not confirm:
                st.error("Please check the confirmation box before continuing.")
            else:
                st.session_state["accepted_terms"] = True
                st.rerun()
    st.stop()

# --- PDF UPLOAD ---
uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
if st.button("Back to Terms", key="back_to_terms"):
    st.session_state["accepted_terms"] = False
    st.rerun()

if uploaded_pdf:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_pdf.read())

    st.info("Extracting text from the document...")
    pages = extract_text_from_pdf("temp.pdf")
    for p in pages:
        p["cleaned_text"] = preprocess_for_llm(p["text"])

    chunks = chunk_document(pages)
    st.success(f"✅ Processed {len(chunks)} chunks")

    st.info("Creating Vector Store...")
    llm_model, query_gen_llm = configure_genai()

    vectorstore = create_vector_store(chunks, "uploaded_report")
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

    from langchain_classic.retrievers import MultiQueryRetriever
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever, llm=query_gen_llm
    )
    st.success("Vector Store and Retriever ready!")

    # Session state
    if "summaries" not in st.session_state:
        st.session_state["summaries"] = None
    if "translated_summaries" not in st.session_state:
        st.session_state["translated_summaries"] = None
    if "translated_lang_code" not in st.session_state:
        st.session_state["translated_lang_code"] = None

    # --- Generate Summaries ---
    if st.button("🚀 Generate Summaries"):
        with st.spinner("Generating summaries..."):
            summaries = summarize_all_sections(multi_query_retriever, llm_model)
            st.session_state["summaries"] = summaries
            st.session_state["translated_summaries"] = None
            st.success("Summaries generated successfully!")

    summaries = st.session_state.get("summaries")
    if summaries:
        st.markdown("## 🧾 Generated Summaries")
        for section, summary in summaries.items():
            st.subheader(section)
            st.write(summary)

        # Download summaries as PDF
        pdf_bytes = create_pdf_pdfkit(summaries, title="Generated Summaries")
        st.download_button(
            "📥 Download Generated Summaries (PDF)",
            data=pdf_bytes,
            file_name="generated_summaries.pdf",
            mime="application/pdf",
        )

        # English Audio
        if _AUDIO_MODULE_AVAILABLE:
            if st.button("🔊 Generate Audio (English)"):
                with st.spinner("Generating audio..."):
                    text = "\n\n".join([f"{sec}\n{txt}" for sec, txt in summaries.items()])
                    audio_path = audio_module.generate_audio_from_text(text=text, lang="en")
                    st.audio(audio_path)

        # --- GLOBAL TRANSLATION ---
        if _TRANSLATE_MODULE_AVAILABLE:
            lang_map = translate_module._get_language_map()
            options = sorted(lang_map.keys())
            st.markdown("---")
            st.markdown("### 🌐 Translate All Summaries")
            col_a, col_b = st.columns([3, 1])
            with col_a:
                default_index = options.index("English") if "English" in options else 0
                dest_name = st.selectbox(
                    "Target language",
                    options,
                    index=default_index,
                    key="global_translate_lang",
                )
            with col_b:
                translate_all_btn = st.button("Translate all")

            if translate_all_btn:
                dest_code = lang_map.get(dest_name)
                translated_summaries = {}
                with st.spinner("Translating summaries..."):
                    for section, summary in summaries.items():
                        translated_summaries[section] = translate_module.translate_text(summary, dest=dest_code)
                st.session_state["translated_summaries"] = translated_summaries
                st.session_state["translated_lang_code"] = dest_code
                st.success("✅ Translation complete")

    # --- Translated Summaries Display (NO PDF DOWNLOAD) ---
    translated_summaries = st.session_state.get("translated_summaries")
    lang_code = st.session_state.get("translated_lang_code")
    if translated_summaries:
        st.markdown("## 🌍 Translated Summaries")
        for section, text in translated_summaries.items():
            st.subheader(section)
            st.write(text)

        # Removed PDF download for translated summaries

        if _AUDIO_MODULE_AVAILABLE:
            if st.button("🔊 Generate Audio (Translated)"):
                with st.spinner("Generating audio..."):
                    all_text = "\n\n".join([f"{sec}\n{txt}" for sec, txt in translated_summaries.items()])
                    audio_path = audio_module.generate_audio_from_text(text=all_text, lang=lang_code)
                    st.audio(audio_path)
