# Voice-Driven SaaS MVP Backend

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI App                          │
├─────────────┬─────────────┬─────────────┬─────────────────┤
│  /voice     │  /documents │  /entries   │  /transactions  │
│  - transcribe│  - upload   │  - CRUD     │  - CRUD         │
│             │  - OCR      │  - list     │  - summary      │
├─────────────┴─────────────┴─────────────┴─────────────────┤
│                      Service Layer                          │
├─────────────┬─────────────┬────────────────────────────────┤
│ WhisperSvc  │ OCRService  │ ExtractionService              │
│ (transcribe)│ (document)  │ (structured data)              │
├─────────────┴─────────────┴────────────────────────────────┤
│                    Data Access Layer                        │
├─────────────┬─────────────┬────────────────────────────────┤
│  Document   │   Entry     │ Transaction                    │
│  Model      │   Model     │ Model                          │
├─────────────┴─────────────┴────────────────────────────────┤
│                   PostgreSQL Database                       │
└─────────────────────────────────────────────────────────────┘
```

## Setup

```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@localhost:5432/voice_saas
export OPENAI_API_KEY=sk-...
uvicorn app.main:app --reload
```

## API Documentation

Visit http://localhost:8000/docs for Swagger UI

## Models

### Document
- id: UUID
- filename: str
- file_path: str
- ocr_text: Optional[str]
- extracted_data: JSONB
- status: enum(pending, processing, completed, failed)
- created_at: datetime

### Entry
- id: UUID
- type: enum(text, voice, document)
- content: str
- source_document_id: Optional[UUID] FK
- metadata: JSONB
- created_at: datetime

### Transaction
- id: UUID
- entry_id: UUID FK
- amount: Decimal
- category: str
- description: str
- date: date
- created_at: datetime
