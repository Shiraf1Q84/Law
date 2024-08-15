import streamlit as st
import pinecone
from sentence_transformers import SentenceTransformer
import os

# Pineconeの設定
pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENVIRONMENT")
index_name = "copyright-laws"

# センテンスBERTモデルのロード
@st.cache(allow_output_mutation=True)
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_model()

# 法文データ（実際にはもっと大規模なものを使用）
legal_texts = [
    "著作権法第1条 この法律は、著作物並びに実演、レコード、放送及び有線放送に関し著作者の権利及びこれに隣接する権利を定め、これらの文化的所産の公正な利用に留意しつつ、著作者等の権利の保護を図り、もつて文化の発展に寄与することを目的とする。",
    "著作権法第2条 この法律において、次の各号に掲げる用語の意義は、当該各号に定めるところによる。",
    "著作権法第10条 この法律にいう著作物を例示すると、おおむね次のとおりである。",
    # ... 他の法文を追加 ...
]

def setup_pinecone():
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=384, metric="cosine")
    
    index = pinecone.Index(index_name)
    
    for i, text in enumerate(legal_texts):
        vector = model.encode(text).tolist()
        index.upsert([(str(i), vector, {"text": text})])

def search_relevant_laws(query):
    query_vector = model.encode(query).tolist()
    
    index = pinecone.Index(index_name)
    results = index.query(query_vector, top_k=3, include_metadata=True)
    
    relevant_laws = [match['metadata']['text'] for match in results['matches']]
    return relevant_laws

def main():
    st.title("著作権法検索アプリケーション")

    st.sidebar.header("アプリケーション情報")
    st.sidebar.info("このアプリケーションは、自然言語処理を使用して著作権法に関連する法文を検索します。")

    if st.sidebar.button("データベースの初期化"):
        with st.spinner("データベースを初期化中..."):
            setup_pinecone()
        st.sidebar.success("データベースの初期化が完了しました！")

    st.write("検索したいキーワードや文章を入力してください。")

    query = st.text_input("検索クエリ:")

    if st.button("検索"):
        if query:
            with st.spinner("関連する法文を検索中..."):
                results = search_relevant_laws(query)
            
            st.subheader("関連する法文:")
            for i, law in enumerate(results, 1):
                st.write(f"{i}. {law}")
                st.markdown("---")
        else:
            st.warning("検索クエリを入力してください。")

if __name__ == "__main__":
    main()