from rag.vector_store import get_vector_store
from rag.db_loader import load_users


def update_user_embeddings():

    documents = load_users()
    vector_store = get_vector_store()

    try:
        print("Resetting RAG collection...")
        vector_store.reset_collection()
    except Exception as e:
        print(f"Error resetting collection: {e}")

    # Re-initialize to pick up the new collection ID
    vector_store = get_vector_store(force_reload=True)

    if documents:
        print(f"Adding {len(documents)} new documents...")
        vector_store.add_texts(documents)
        print("Embeddings updated successfully.")