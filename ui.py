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
         if original_query:
            if use_improved_query:
                with st.spinner("検索クエリを改善中..."):
                    improved_query, explanation = query_generator(original_query, api_key)
                
                if improved_query is None:
                    st.error(f"エラーが発生しました: {explanation}")
                    return

                st.subheader("検索クエリの改善")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info("元のクエリ")
                    st.write(original_query)
                with col2:
                    st.success("改善されたクエリ")
                    st.write(improved_query)

                with st.expander("改善プロセスの詳細"):
                    st.write(explanation)
            else:
                improved_query = original_query

            search_results_placeholder = st.empty()
            progress_bar = st.progress(0)

            with st.spinner("検索中..."):
                if use_improved_query:
                    original_results = search_engine.search(original_query)
                    improved_results = search_engine.search(improved_query)
                    all_results = list(set(original_results + improved_results))
                else:
                    all_results = search_engine.search(original_query)
                
                # スコアでソート
                all_results.sort(key=lambda x: x['score'], reverse=True)
            
            if all_results:
                st.subheader("検索結果")
                for i, result in enumerate(all_results):
                    with st.expander(f"結果 {i+1} - スコア: {result['score']:.2f}"):
                        st.markdown(f"<span style='color: #A0A0A0;'><strong>ファイル名: {result['document']['file_name']}</strong></span>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color: #A0A0A0;'><strong>ページ番号: {result['document']['page_number']}</strong></span>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color: #A0A0A0;'><strong>チャンク番号: {result['document']['chunk_number']}</strong></span>", unsafe_allow_html=True)
                        
                        # クエリソースを表示（改善クエリを使用している場合のみ）
                        if use_improved_query:
                            if result in original_results and result in improved_results:
                                st.markdown("<span style='color: #FFA500;'><strong>元のクエリと改善されたクエリの両方でヒット</strong></span>", unsafe_allow_html=True)
                            elif result in original_results:
                                st.markdown("<span style='color: #1E90FF;'><strong>元のクエリでヒット</strong></span>", unsafe_allow_html=True)
                            else:
                                st.markdown("<span style='color: #32CD32;'><strong>改善されたクエリでヒット</strong></span>", unsafe_allow_html=True)
                        
                        # テキストを表示
                        st.markdown(result['document']['text'])
                        
                        # 画像を表示
                        if 'images' in result['document'] and result['document']['images']:
                            st.subheader("ページ内の画像")
                            for img in result['document']['images']:
                                image_data = base64.b64decode(img['base64'])
                                image = Image.open(io.BytesIO(image_data))
                                st.image(image, caption=f"画像 {img['index'] + 1}", use_column_width=True)
                        
                        st.markdown("---")
                    
                    # 進捗バーの更新
                    progress = (i + 1) / len(all_results)
                    progress_bar.progress(progress)
                
                progress_bar.empty()
            else:
                st.warning("検索結果が見つかりませんでした。")
        else:
            st.warning("検索ワードを入力してください。")

if __name__ == "__main__":
    db = VectorDatabase()
    engine = SearchEngine(db)
    run_ui(engine, generate_improved_query)
