from rag.retriever import retrieve_context


def rag_answer(query, llm):

    context = retrieve_context(query)

    prompt = f"""
Context:
{context}

Answer the question using the context above.

Question:
{query}
"""

    return llm.invoke(prompt)