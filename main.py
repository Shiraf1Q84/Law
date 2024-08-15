import streamlit as st
import pypdf
from sentence_transformers import SentenceTransformer
import pinecone
import os
import tempfile

# Streamlitの設定
st.set_page_config(page_title="PDF to Vector Database", layout="wide")

# Pineconeの初期化
if 'pinecone_initialized' not in st.session_state:
    st.session_state.pinecone_initialized = False

# SentenceTransformerモデルの読み込み
@st.cache_resource
def load_model():
    return SentenceTransformer('sonoisa/sentence-bert-base-ja-mean-tokens')

model = load_model()

def extract_text_from_pdf(file):
    pdf_reader = pypdf.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def create_embeddings(text, chunk_size=1000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    embeddings = model.encode(chunks)
    return chunks, embeddings

def upload_to_pinecone(chunks, embeddings, index_name):
    index = pinecone.Index(index_name)
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        i_end = min(i+batch_size, len(chunks))
        ids = [str(j) for j in range(i, i_end)]
        metadatas = [{"text": chunk} for chunk in chunks[i:i_end]]
        vectors = embeddings[i:i_end].tolist()
        index.upsert(vectors=zip(ids, vectors, metadatas))

def main():
    st.title("PDF to Vector Database Converter")

    # サイドバーでPinecone設定
    with st.sidebar:
        st.header("Pinecone Settings")
        api_key = st.text_input("API Key", type="password")
        environment = st.text_input("Environment")
        index_name = st.text_input("Index Name")

        if st.button("Initialize Pinecone"):
            if api_key and environment and index_name:
                try:
                    pinecone.init(api_key=api_key, environment=environment)
                    if index_name not in pinecone.list_indexes():
                        pinecone.create_index(index_name, dimension=768, metric="cosine")
                    st.session_state.pinecone_initialized = True
                    st.success("Pinecone initialized successfully!")
                except Exception as e:
                    st.error(f"Error initializing Pinecone: {str(e)}")
            else:
                st.warning("Please fill in all Pinecone settings.")

    # メイン画面
    if st.session_state.pinecone_initialized:
        st.write("Drag and drop your PDF files here:")
        uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                with st.spinner(f'Processing {uploaded_file.name}...'):
                    # PDFからテキストを抽出
                    text = extract_text_from_pdf(tmp_file_path)
                    st.write(f"Extracted {len(text)} characters from {uploaded_file.name}")

                    # テキストを埋め込みベクトルに変換
                    chunks, embeddings = create_embeddings(text)
                    st.write(f"Created {len(chunks)} chunks and embeddings")

                    # Pineconeにアップロード
                    upload_to_pinecone(chunks, embeddings, index_name)
                    st.success(f"Successfully uploaded embeddings for {uploaded_file.name} to Pinecone!")

                os.unlink(tmp_file_path)  # 一時ファイルを削除

    else:
        st.warning("Please initialize Pinecone first.")

if __name__ == "__main__":
    main()
