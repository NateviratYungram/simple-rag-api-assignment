from pathlib import Path
from typing import List

import fitz


def load_txt(file_path: Path) -> List[dict]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    return [{"page": None, "text": text}]


def load_pdf(file_path: Path) -> List[dict]:
    pages: List[dict] = []
    with fitz.open(file_path) as document:
        for index, page in enumerate(document, start=1):
            text = page.get_text("text")
            if text.strip():
                pages.append({"page": index, "text": text})
    return pages


def load_document(file_path: Path) -> List[dict]:
    suffix = file_path.suffix.lower()
    if suffix == ".txt":
        return load_txt(file_path)
    if suffix == ".pdf":
        return load_pdf(file_path)
    raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")

