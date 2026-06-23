from typing import List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class IngestResponse(BaseModel):
    status: str
    file_name: str
    chunks_indexed: int


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Question to ask about the indexed documents.")


class SourceItem(BaseModel):
    file_name: str
    text: str
    page: Optional[int] = None
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceItem]

