# pdf_processor.py
import fitz  # PyMuPDF
from typing import List
import os

def process_pdf(file_path: str) -> List[dict]:
    chunks = []
    doc = fitz.open(file_path)
    file_name = os.path.basename(file_path)
    for page in doc:
        text = page.get_text()
        chunks.extend(split_into_chunks(text, file_name, page.number))
    return chunks

def split_into_chunks(text: str, file_name: str, page_number: int) -> List[dict]:
    chunk_size = 1000  # 例として1000文字ごとに分割
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = {
            'text': text[i:i+chunk_size],
            'file_name': file_name,
            'page_number': page_number,
            'chunk_number': i // chunk_size + 1
        }
        chunks.append(chunk)
    return chunks
