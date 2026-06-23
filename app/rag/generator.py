from app.rag.embedder import get_openai_client
from app.rag.prompts import SYSTEM_PROMPT, build_user_prompt
from app.config import settings


def generate_answer(query: str, context_chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"Source {index + 1} | file={item['file_name']} | page={item.get('page')}\n{item['text']}"
        for index, item in enumerate(context_chunks)
    )

    client = get_openai_client()
    response = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(query, context)},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or "No answer generated."

