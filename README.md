# Simple RAG API

A simple Retrieval-Augmented Generation (RAG) API built for an assignment. The service accepts PDF or TXT documents, indexes their content, and answers user questions with source references.

## Overview

This project implements a minimal RAG pipeline with three main steps:

1. Ingest a document
2. Convert the document into searchable vector embeddings
3. Answer questions using only retrieved document context

## Features

- Upload PDF or TXT documents
- Extract and chunk text
- Generate embeddings and store vectors locally
- Retrieve relevant chunks for a user query
- Generate grounded answers with source references

## Tech Stack

- Python
- FastAPI
- OpenAI API
- NumPy
- PyMuPDF

## Architecture

```mermaid
flowchart TD
    A["Client"] --> B["POST /ingest"]
    B --> C["Document Loader"]
    C --> D["Text Chunker"]
    D --> E["Embedding Model"]
    E --> F["Local Vector Store"]

    A --> G["POST /ask"]
    G --> H["Query Embedding"]
    H --> I["Retriever"]
    F --> I
    I --> J["Relevant Chunks"]
    J --> K["LLM Generator"]
    K --> L["Answer + Sources"]
```

## Project Structure

```text
rag-assignment/
  app/
    api/
    rag/
    services/
    storage/
    config.py
    main.py
    schemas.py
  data/
    uploads/
    index/
  .env.example
  .gitignore
  README.md
  requirements.txt
```

## Setup

1. Create a virtual environment
2. Install dependencies
3. Copy `.env.example` to `.env`
4. Add your OpenAI API key

```bash
pip install -r requirements.txt
```

Recommended Python version: `3.11+`

## Environment Variables

```env
OPENAI_API_KEY=your_api_key_here
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
CHUNK_SIZE=800
CHUNK_OVERLAP=150
TOP_K=4
```

## Run Locally

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive API docs:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## API Endpoints

### `GET /health`

Returns the service status.

Response:

```json
{
  "status": "ok"
}
```

### `POST /ingest`

Uploads a PDF or TXT document and indexes it for retrieval.

Request:
- `multipart/form-data`
- field name: `file`

Response:

```json
{
  "status": "success",
  "file_name": "sample.pdf",
  "chunks_indexed": 12
}
```

Notes:

- Supported file types: `pdf`, `txt`
- The uploaded file is stored locally in `data/uploads/`
- Vector data and metadata are stored in `data/index/`

### `POST /ask`

Accepts a user query and returns an answer based on indexed document content.

Request:

```json
{
  "query": "What is this document about?"
}
```

Response:

```json
{
  "answer": "The document explains ...",
  "sources": [
    {
      "file_name": "sample.pdf",
      "page": 1,
      "text": "Relevant content from the document...",
      "score": 0.1234
    }
  ]
}
```

Behavior:

- If no document has been indexed yet, the API returns an error
- If no relevant context is found, the API returns an answer indicating that the information was not found in the document

## Example Usage

Ingest a document:

```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@sample.pdf"
```

Ask a question:

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"Summarize this document\"}"
```

## Running Tests

```bash
pytest
```

## Limitations

- Local single-instance storage only
- Basic character-based chunking
- No authentication
- No document deletion or re-index workflow yet

## Future Improvements

- Add support for multiple document collections
- Improve chunking with token-aware splitting
- Add tests and CI
- Add Docker support

## Submission Notes

This repository is structured to satisfy the assignment requirements:

- RAG pipeline for PDF/TXT documents
- At least one query endpoint
- Answer response with source references
- README with setup and usage instructions
