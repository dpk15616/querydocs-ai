from functools import lru_cache
from typing import List

from langchain_groq import ChatGroq
from app.retriever import load_vector_store


@lru_cache(maxsize=1)
def get_llm():
    """Cache LLM instance to avoid reinitializing on every query."""
    return ChatGroq(model="llama-3.3-70b-versatile")


def get_rag_response(query: str, chat_history: List = None):
    if chat_history is None:
        chat_history = []
    
    db = load_vector_store()
    docs = db.similarity_search(query, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    llm = get_llm()

    history_text = ""
    if chat_history:
        history_text = "Previous conversation:\n"
        for msg in chat_history[-6:]:
            role = "User" if msg.role == "user" else "Assistant"
            history_text += f"{role}: {msg.content}\n"
        history_text += "\n"

    prompt = f"""
{history_text}Answer using ONLY the context below. If the question refers to previous conversation, use that context to understand the question better.

Context:
{context}

Current Question: {query}
"""

    response = llm.invoke(prompt)
    return response.content
