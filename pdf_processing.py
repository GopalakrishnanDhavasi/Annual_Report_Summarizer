import fitz
import re
from typing import List, Dict, Union
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, Union[int, str]]]:
    doc = fitz.open(pdf_path)
    pages_data = [{'page_number': i + 1, 'text': page.get_text()} for i, page in enumerate(doc)]
    doc.close()
    return pages_data

def preprocess_for_llm(text: str) -> str:
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def chunk_document(processed_pages: List[Dict[str, Union[int, str]]]):
    full_text = ""
    for page in processed_pages:
        page_separator = f"\n\n--- PAGE {page['page_number']} ---\n\n"
        full_text += page_separator + page['cleaned_text']

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1600, chunk_overlap=200, length_function=len,
        is_separator_regex=True, separators=[r"\n\n--- PAGE \d+ ---\n\n", "\n\n", "\n", " ", ""]
    )
    chunks = splitter.create_documents([full_text])
    final_chunks = []
    for chunk in chunks:
        chunk.page_content = re.sub(r"--- PAGE \d+ ---", "", chunk.page_content).strip()
        chunk.metadata = {}
        final_chunks.append(chunk)
    return final_chunks
