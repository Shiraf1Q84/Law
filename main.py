import streamlit as st
import pinecone
from sentence_transformers import SentenceTransformer
import os

# Pineconeの設定をセッションステートに保存
if 'pinecone_initialized' not in st.session_state:
    st.session_state.pinecone_initialized = False

# 日本語特化センテンスBERTモデルのロード
@st.cache(allow_output_mutation=True)
def load_model():
    return SentenceTransformer('sonoisa/sentence-bert-base-ja-mean-tokens')

model = load_model()

# 法文データ（実際にはもっと大規模なものを使用）
legal_texts = [
    "著作権法第1条 この法律は、著作物並びに実演、レコード、放送及び有線放送に関し著作者の権利及びこれに隣接する権利を定め、これらの文化的所産の公正な利用に留意しつつ、著作者等の権利の保護を図り、もつて文化の発展に寄与することを目的とする。",
    "著作権法第2条 この法律において、次の各号に掲げる用語の意義は、当該各号に定めるところによる。",
    "著作権法第10条 この法律にいう著作物を例示すると、おおむね次のとおりである。",
    # ... 他の法文を追加 ...
]

def setup_pinecone(index_name):
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=768, metric="cosine")
    
    index = pinecone.Index(index_name)
    
    for i, text in enumerate(legal_texts):
        vector = model.encode(text).tolist()
        index.upsert([(str(i), vector, {"text": text})])

def search_relevant_laws(query, index_name):
    query_vector = model.encode(query).tolist()
    
    index = pinecone.Index(index_name)
    results = index.query(query_vector, top_k=3, include_metadata=True)
    
    relevant_laws = [match['metadata']['text'] for match in results['matches']]
    return relevant_laws

def main():
    st.title("著作権法検索アプリケーション")

    # Pinecone設定入力フォーム
    st.sidebar.header("Pinecone設定")
    api_key = st.sidebar.text_input("Pinecone API Key", type="password")
    environment = st.sidebar.text_input("Pinecone Environment")
    index_name = st.sidebar.text_input("Pinecone Index Name", value="copyright-laws")

    # Pinecone初期化ボタン
    if st.sidebar.button("Pineconeを初期化"):
        if api_key and environment:
            try:
                pinecone.init(api_key=api_key, environment=environment)
                st.session_state.pinecone_initialized = True
                st.sidebar.success("Pineconeが正常に初期化されました。")
            except Exception as e:
                st.sidebar.error(f"Pineconeの初期化に失敗しました: {str(e)}")
        else:
            st.sidebar.warning("API KeyとEnvironmentを入力してください。")

    if st.session_state.pinecone_initialized:
        if st.sidebar.button("データベースの初期化"):
            with st.spinner("データベースを初期化中..."):
                setup_pinecone(index_name)
            st.sidebar.success("データベースの初期化が完了しました！")

        st.write("検索したいキーワードや文章を入力してください。")

        query = st.text_input("検索クエリ:")

        if st.button("検索"):
            if query:
                with st.spinner("関連する法文を検索中..."):
                    results = search_relevant_laws(query, index_name)
                
                st.subheader("関連する法文:")
                for i, law in enumerate(results, 1):
                    st.write(f"{i}. {law}")
                    st.markdown("---")
            else:
                st.warning("検索クエリを入力してください。")
    else:
        st.warning("Pineconeを初期化してください。")

if __name__ == "__main__":
    main()
