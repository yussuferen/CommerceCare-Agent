import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

DOCS_FOLDER = "docs/pdf"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "ecommerce_support"
EMBEDDING_MODEL = "models/gemini-embedding-2-preview"

def read_and_chunk_pdf():
    loader = PyPDFDirectoryLoader(DOCS_FOLDER)
    documents = loader.load()
        
    print(f"Found {len(documents)} PDF pages to process.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def get_embedding_function():
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )


def load_vector_db():
    print("Loading existing ChromaDB database from disk...")
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=get_embedding_function(),
        collection_name=COLLECTION_NAME
    )


def create_vector_db():
    print("Initial setup: Processing all PDFs and generating embeddings with Gemini API...")

    vectorstore = Chroma.from_documents(
        documents=read_and_chunk_pdf(),
        embedding=get_embedding_function(),
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME
    )
    print(f"Data successfully saved to ChromaDB!")
    return vectorstore


def get_vector_db():
    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
        return load_vector_db()
    return create_vector_db()