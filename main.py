
# main.py
import pdf_processor
import vector_database
import search_engine
import ui

def main():
    # PDFファイルの処理
    pdf_path = "sample_law.pdf"
    text_chunks = pdf_processor.process_pdf(pdf_path)
    
    # ベクトルデータベースの構築
    db = vector_database.VectorDatabase()
    for chunk in text_chunks:
        db.add_document(chunk)
    
    # 検索エンジンの初期化
    engine = search_engine.SearchEngine(db)
    
    # UIの起動
    ui.run(engine)

if __name__ == "__main__":
    main()