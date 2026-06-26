from app.config import settings
from app.rag.embedder import get_gemini_client
from app.rag.prompts import SYSTEM_PROMPT, build_user_prompt
from google.genai import types


def generate_answer(query: str, context_chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"Source {index + 1} | file={item['file_name']} | page={item.get('page')}\n{item['text']}"
        for index, item in enumerate(context_chunks)
    )

    client = get_gemini_client()
    response = client.models.generate_content(
        model=settings.chat_model,
        contents=build_user_prompt(query, context),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )
    return response.text or "No answer generated."
