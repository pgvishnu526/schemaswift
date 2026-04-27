from langchain_chroma import Chroma
from rag.embeddings import embedding_model

_vector_store = None

def get_vector_store(force_reload=False):
    global _vector_store
    if _vector_store is None or force_reload:
        _vector_store = Chroma(
            collection_name="schemaswift_rag",
            embedding_function=embedding_model,
            persist_directory="./chroma_store"
        )
    return _vector_store