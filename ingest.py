import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def run_ingestion():
    # 1. Check if PDF exists
    pdf_path = "./short_story_pdf.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found in the current directory.")
        return

    print(f"Loading {pdf_path}...")
    
    # 2. Load PDF using the stable PyPDFLoader
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # 3. Split into meaningful chunks
    # Recursive splitter is the 'gold standard' for keeping context together
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(pages)
    print(f"Split document into {len(docs)} chunks.")

    # 4. Create and persist the Vector Database
    print("Generating embeddings and building ChromaDB...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    print("✅ Success! Database created in './chroma_db'.")

if __name__ == "__main__":
    run_ingestion()