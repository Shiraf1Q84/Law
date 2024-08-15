# ui.py
import streamlit as st
from search_engine import SearchEngine

def run_ui(search_engine: SearchEngine):
    st.title("法文横断検索システム")

    query = st.text_input("検索ワードを入力してください")
    if st.button("検索"):
        with st.spinner("検索中..."):
            results = search_engine.search(query)
        
        st.subheader("検索結果")
        for result in results:
            st.write(f"スコア: {result['score']:.2f}")
            st.write(f"ページ番号: {result['document']['page_number']}")
            st.write(f"チャンク番号: {result['document']['chunk_number']}")
            st.write(result['document']['text'])
            st.markdown("---")

if __name__ == "__main__":
    # このブロックは直接ui.pyを実行した場合のためのもので、
    # 通常はmain.pyから呼び出されるため使用されません
    from vector_database import VectorDatabase
    db = VectorDatabase()
    engine = SearchEngine(db)
    run_ui(engine)
