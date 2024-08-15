#pdf_processor.py
from typing import List, Dict
import os
from llama_parse import LlamaParse
import re

def process_pdf(file_path: str, api_key: str) -> List[dict]:
    chunks = []
    file_name = os.path.basename(file_path)
    
    # Set up LlamaParse
    parser = LlamaParse(result_type="markdown", api_key=api_key)
    
    # Parse the PDF
    documents = parser.load_data(file_path)
    
    for page_num, doc in enumerate(documents):
        text = doc.text
        chunks.extend(split_into_chunks(text, file_name, page_num))
    
    return chunks

def split_into_chunks(text: str, file_name: str, page_number: int) -> List[dict]:
    # 文章の区切り（。、！、？）や改行で分割
    sentences = re.split(r'[。！？\n]+', text)
    
    chunks = []
    current_chunk = ''
    chunk_number = 1
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= 1000:
            current_chunk += sentence + '。'
        else:
            chunks.append({
                'text': current_chunk,
                'file_name': file_name,
                'page_number': page_number,
                'chunk_number': chunk_number
            })
            current_chunk = sentence + '。'
            chunk_number += 1
    
    if current_chunk:
        chunks.append({
            'text': current_chunk,
            'file_name': file_name,
            'page_number': page_number,
            'chunk_number': chunk_number
        })
    
    return chunks
