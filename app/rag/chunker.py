from typing import List


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: List[str] = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - chunk_overlap

    return chunks


def build_chunks(document_pages: List[dict], file_name: str, chunk_size: int, chunk_overlap: int) -> List[dict]:
    chunk_records: List[dict] = []
    for page_record in document_pages:
        for chunk in chunk_text(page_record["text"], chunk_size, chunk_overlap):
            chunk_records.append(
                {
                    "file_name": file_name,
                    "page": page_record["page"],
                    "text": chunk,
                }
            )
    return chunk_records

