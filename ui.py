# ui.py
import streamlit as st

def run(search_engine: SearchEngine):
    st.title("法文横断検索システム")

    query = st.text_input("検索ワードを入力してください")
    if st.button("検索"):
        with st.spinner("検索中..."):
            results = search_engine.search(query)
        
        st.subheader("検索結果")
        for result in results:
            st.write(f"類似度: {result['similarity']:.2f}")
            st.write(f"法律名: {result['document']['law_name']}")
            st.write(f"条文番号: {result['document']['article_number']}")
            st.write(result['document']['text'])
            st.markdown("---")