#ui.py
import streamlit as st
from search_engine import SearchEngine
from query_generator import generate_improved_query
from vector_database import VectorDatabase
import time
from config import save_api_keys, load_api_keys, clear_api_keys
from pdf_processor import process_pdf

def run_ui(search_engine: SearchEngine, query_generator):
    st.title("法文横断検索システム")

    # 保存されたAPIキーを読み込む
    openai_api_key, llama_cloud_api_key = load_api_keys()

    # サイドバーにAPIキー関連の設定と検索クエリ改善の設定を配置
    with st.sidebar:
        st.header("設定")
        if not openai_api_key or not llama_cloud_api_key:
            new_openai_api_key = st.text_input("OpenAI APIキーを入力してください", type="password")
            new_llama_cloud_api_key = st.text_input("Llama Cloud APIキーを入力してください", type="password")
            if st.button("APIキーを保存"):
                save_api_keys(new_openai_api_key, new_llama_cloud_api_key)
                openai_api_key = new_openai_api_key
                llama_cloud_api_key = new_llama_cloud_api_key
                st.success("APIキーが保存されました。")
        else:
            st.success("APIキーが設定されています。")
            if st.button("APIキーをリセット"):
                clear_api_keys()
                openai_api_key = ""
                llama_cloud_api_key = ""
                st.warning("APIキーがリセットされました。新しいキーを入力してください。")
        
        # 検索クエリ改善の設定を追加
        use_improved_query = st.checkbox("検索クエリの改善を使用する", value=True)

    if not openai_api_key or not llama_cloud_api_key:
        st.warning("OpenAI APIキーとLlama Cloud APIキーを設定してください。")
        return

    # PDFファイルのアップロード
    uploaded_files = st.file_uploader("PDFファイルをアップロードしてください", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            text_chunks = process_pdf(uploaded_file, llama_cloud_api_key)
            for chunk in text_chunks:
                search_engine.db.add_document(chunk)
        st.success("PDFファイルが処理されました。")

    # メイン検索インターフェース
    original_query = st.text_input("検索ワードを入力してください")
    if st.button("検索"):
        # 検索処理は前のコードと同じ
        # ...

if __name__ == "__main__":
    db = VectorDatabase()
    engine = SearchEngine(db)
    run_ui(engine, generate_improved_query)
