# pdf_processor.py
import fitz  # PyMuPDF
from typing import List

def process_pdf(file_path: str) -> List[dict]:
    chunks = []
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        # テキストを適切なサイズのチャンクに分割
        # メタ情報（ページ番号など）を追加
        chunks.extend(split_into_chunks(text, page.number))
    return chunks

def split_into_chunks(text: str, page_number: int) -> List[dict]:
    # テキストを適切なサイズのチャンkに分割するロジック
    # 各チャンクにメタ情報を付与
    pass