SYSTEM_PROMPT = """You answer questions using only the provided document context.
If the answer is not present in the context, say that the information was not found in the document.
Keep the answer concise and grounded in the source material."""


def build_user_prompt(question: str, context: str) -> str:
    return f"""Context:
{context}

Question:
{question}

Answer using only the context above."""

