from rag.retriever import retrieve_context
from llm.prompts import RAG_PROMPT_TEMPLATE
from llm.intent_router import call_llm


def generate_rag_response(query: str):

    """
    Generate natural-language answer using RAG pipeline
    """

    context = retrieve_context(query)

    if not context:
        return {
            "success": False,
            "message": "No relevant information found."
        }

    prompt = RAG_PROMPT_TEMPLATE.format(
        context=context,
        question=query
    )

    answer = call_llm(prompt)

    return {
        "success": True,
        "mode": "rag",
        "answer": answer,
        "source": "PostgreSQL tables (users, access_requests, activity_logs)"
    }