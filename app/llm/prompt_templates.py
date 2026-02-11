def build_rag_prompt(context: dict) -> str:
    """
    Constructs final prompt for RAG.
    """

    query = context["query"]
    retrieved = context["retrieved_content"].get("chunks", [])
    chat_history = context.get("chat_history", [])

    retrieved_text = "\n\n".join(
        chunk["text"] for chunk in retrieved
    )

    history_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in chat_history
    )

    prompt = f"""
You are an intelligent assistant.

Use the provided context to answer the question.
If the answer is not found in context, say you do not know.

Conversation History:
{history_text}

Retrieved Context:
{retrieved_text}

User Question:
{query}

Answer:
"""

    return prompt
