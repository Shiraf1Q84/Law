# main.py
from pdf_processor import process_pdf
from vector_database import VectorDatabase
from search_engine import SearchEngine
from ui import run_ui

def main():
    # PDFファイルの処理
    pdf_path = "sample_law.pdf"
    text_chunks = process_pdf(pdf_path)
    
    # ベクトルデータベースの構築
    db = VectorDatabase()
    for chunk in text_chunks:
        db.add_document(chunk)
    
    # 検索エンジンの初期化
    engine = SearchEngine(db)
    
    # UIの起動
    run_ui(engine)

if __name__ == "__main__":
    main()
