# pdf_processor.py
import fitz  # PyMuPDF
from typing import List

def process_pdf(file_path: str) -> List[dict]:
    chunks = []
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        chunks.extend(split_into_chunks(text, page.number))
    return chunks

def split_into_chunks(text: str, page_number: int) -> List[dict]:
    chunk_size = 1000  # 例として1000文字ごとに分割
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = {
            'text': text[i:i+chunk_size],
            'page_number': page_number,
            'chunk_number': i // chunk_size + 1
        }
        chunks.append(chunk)
    return chunks
