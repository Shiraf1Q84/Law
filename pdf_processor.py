# # pdf_processor.py
# import fitz  # PyMuPDF
# from typing import List
# import os

# def process_pdf(file_path: str) -> List[dict]:
#     chunks = []
#     doc = fitz.open(file_path)
#     file_name = os.path.basename(file_path)
#     for page in doc:
#         text = page.get_text()
#         chunks.extend(split_into_chunks(text, file_name, page.number))
#     return chunks

# def split_into_chunks(text: str, file_name: str, page_number: int) -> List[dict]:
#     chunk_size = 1000  # 例として1000文字ごとに分割
#     chunks = []
#     for i in range(0, len(text), chunk_size):
#         chunk = {
#             'text': text[i:i+chunk_size],
#             'file_name': file_name,
#             'page_number': page_number,
#             'chunk_number': i // chunk_size + 1
#         }
#         chunks.append(chunk)
#     return chunks




import fitz  # PyMuPDF
from typing import List, Dict
import os
import base64
from PIL import Image
import io

def process_pdf(file_path: str) -> List[dict]:
    chunks = []
    doc = fitz.open(file_path)
    file_name = os.path.basename(file_path)
    
    for page_num, page in enumerate(doc):
        text = page.get_text()
        images = extract_images(page)
        chunks.extend(split_into_chunks(text, file_name, page_num, images))
    
    return chunks

def extract_images(page: fitz.Page) -> List[Dict[str, str]]:
    images = []
    img_list = page.get_images(full=True)
    
    for img_index, img in enumerate(img_list):
        xref = img[0]
        base_image = page.parent.extract_image(xref)
        image_bytes = base_image["image"]
        
        # Convert image bytes to base64 string
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        images.append({
            "index": img_index,
            "base64": image_base64
        })
    
    return images

def split_into_chunks(text: str, file_name: str, page_number: int, images: List[Dict[str, str]]) -> List[dict]:
    chunk_size = 1000  # 例として1000文字ごとに分割
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = {
            'text': text[i:i+chunk_size],
            'file_name': file_name,
            'page_number': page_number,
            'chunk_number': i // chunk_size + 1,
            'images': images
        }
        chunks.append(chunk)
    return chunks
