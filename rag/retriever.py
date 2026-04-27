from rag.vector_store import get_vector_store


def retrieve_context(query):
    try:
        # Force reload to ensure we see updates from other processes
        vector_store = get_vector_store(force_reload=True)
        results = vector_store.similarity_search(query)
        return "\n".join(
            doc.page_content for doc in results
        )
    except Exception as e:
        print(f"RAG Retrieval error: {e}")
        return ""