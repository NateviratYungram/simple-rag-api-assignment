from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas import AskRequest, AskResponse, HealthResponse, IngestResponse
from app.services.ingest_service import ingest_document
from app.services.query_service import answer_query


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse()


@router.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...)) -> IngestResponse:
    try:
        result = ingest_document(file)
        return IngestResponse(**result)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        result = answer_query(request.query)
        return AskResponse(**result)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

