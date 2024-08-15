# main.py
from pdf_processor import process_pdf
from vector_database import VectorDatabase
from search_engine import SearchEngine
from ui import run_ui
import os

def main():
    # PDFファイルの処理
    pdf_directory = "pdf_files"
    db = VectorDatabase()
    
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_directory, filename)
            text_chunks = process_pdf(file_path)
            for chunk in text_chunks:
                db.add_document(chunk)
    
    # 検索エンジンの初期化
    engine = SearchEngine(db)
    
    # UIの起動
    run_ui(engine)

if __name__ == "__main__":
    main()
