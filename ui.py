# ui.py
import streamlit as st
from search_engine import SearchEngine
from query_generator import generate_improved_query

def run_ui(search_engine: SearchEngine):
    st.title("法文横断検索システム")

    # サイドバーにAPIキー入力欄を追加
    api_key = st.sidebar.text_input("OpenAI APIキーを入力してください", type="password")
    
    if not api_key:
        st.warning("OpenAI APIキーを入力してください。")
        return

    original_query = st.text_input("検索ワードを入力してください")
    if st.button("検索"):
        if original_query:
            with st.spinner("検索クエリを改善中..."):
                improved_query, explanation = generate_improved_query(original_query, api_key)
            
            if "エラーが発生しました" in explanation:
                st.error(explanation)
                return

            st.subheader("検索クエリの改善")
            st.write(f"元のクエリ: {original_query}")
            st.write(f"改善されたクエリ: {improved_query}")
            st.write("改善プロセス:")
            st.write(explanation)

            use_improved = st.radio("使用するクエリを選択してください:", ("元のクエリ", "改善されたクエリ"))
            query = improved_query if use_improved == "改善されたクエリ" else original_query

            with st.spinner("検索中..."):
                results = search_engine.search(query)
            
            if results:
                st.subheader("検索結果")
                for result in results:
                    st.write(f"スコア: {result['score']:.2f}")
                    st.write(f"ファイル名: {result['document']['file_name']}")
                    st.write(f"ページ番号: {result['document']['page_number']}")
                    st.write(f"チャンク番号: {result['document']['chunk_number']}")
                    st.write(result['document']['text'])
                    st.markdown("---")
            else:
                st.warning("検索結果が見つかりませんでした。")
        else:
            st.warning("検索ワードを入力してください。")

if __name__ == "__main__":
    from vector_database import VectorDatabase
    db = VectorDatabase()
    engine = SearchEngine(db)
    run_ui(engine)
