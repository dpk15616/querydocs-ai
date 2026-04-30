import os
from functools import lru_cache

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import VECTOR_DB_PATH


@lru_cache(maxsize=1)
def get_embeddings():
    """Cache embeddings model to avoid reloading on every query."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_vector_store(docs):
    embeddings = get_embeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTOR_DB_PATH)
    get_embeddings.cache_clear()
    return db


def vector_store_exists() -> bool:
    return os.path.isfile(os.path.join(VECTOR_DB_PATH, "index.faiss"))


_vector_store_cache = None


def load_vector_store():
    global _vector_store_cache
    
    if not vector_store_exists():
        raise FileNotFoundError(
            "No documents have been indexed yet. Please upload a PDF first."
        )
    
    if _vector_store_cache is None:
        embeddings = get_embeddings()
        _vector_store_cache = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    
    return _vector_store_cache


def clear_vector_store_cache():
    """Clear the cached vector store (call after uploading new documents)."""
    global _vector_store_cache
    _vector_store_cache = None
