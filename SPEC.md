# Voice-Driven SaaS Platform MVP - Architecture Specification

## Overview

This MVP backend provides a voice-driven interface for financial tracking and document management. The system accepts voice input (transcribed via Whisper), processes document uploads (with OCR via Tesseract), and organizes data in spreadsheet-style entries with financial transaction tracking.

## Technology Stack

- **Framework**: FastAPI (async)
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Voice Processing**: OpenAI Whisper (with mock fallback)
- **OCR**: Tesseract via pytesseract
- **Data Validation**: Pydantic v2

## Architecture Principles

1. **Separation of Concerns**: Routers handle HTTP, Services handle business logic, Models handle data
2. **Async Throughout**: All database operations use async SQLAlchemy
3. **Configuration**: Environment-based configuration with validation
4. **Error Handling**: Structured error responses with proper HTTP status codes

## Directory Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry, CORS, middleware
│   ├── config.py            # Settings from environment
│   ├── database.py          # Async PostgreSQL connection
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── routers/             # API endpoint handlers
│   ├── services/            # Business logic (Whisper, OCR, Extraction)
│   └── utils/               # Helper functions
├── requirements.txt
└── README.md
```

## Database Models

### Document
Stores uploaded documents with OCR results and extracted data.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| filename | String | Original filename |
| file_path | String | Server storage path |
| ocr_text | Text | Raw OCR output |
| extracted_data | JSONB | Structured extraction results |
| status | Enum | pending/processing/completed/failed |
| created_at | DateTime | Timestamp |

### Entry
Spreadsheet-style data entries that can originate from voice, text, or documents.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| type | Enum | text/voice/document |
| content | Text | Main content/text |
| source_document_id | UUID | FK to Document (nullable) |
| metadata | JSONB | Additional context |
| created_at | DateTime | Timestamp |

### Transaction
Financial transactions derived from entries.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| entry_id | UUID | FK to Entry |
| amount | Decimal | Monetary value |
| category | String | Transaction category |
| description | String | Transaction description |
| date | Date | Transaction date |
| created_at | DateTime | Timestamp |

## API Endpoints

### Voice Transcription
- `POST /api/voice/transcribe` - Accept audio file, return transcription

### Document Processing
- `POST /api/documents/upload` - Upload document, run OCR, extract data
- `GET /api/documents/{id}` - Get document by ID
- `GET /api/documents` - List documents with optional status filter

### Entries (Spreadsheet-style CRUD)
- `GET /api/entries` - List all entries
- `POST /api/entries` - Create new entry
- `GET /api/entries/{id}` - Get entry by ID
- `PUT /api/entries/{id}` - Update entry
- `DELETE /api/entries/{id}` - Delete entry

### Transactions
- `GET /api/transactions` - List transactions with optional filters
- `POST /api/transactions` - Create transaction
- `GET /api/transactions/{id}` - Get transaction by ID
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction
- `GET /api/transactions/summary` - Get financial summary/calculations

## Services

### WhisperService
Transcribes audio files to text using OpenAI Whisper API.
- `transcribe(audio_path: str) -> str`: Returns transcription text
- Falls back to mock transcription when API unavailable

### OCRService
Processes documents using Tesseract OCR.
- `process_document(file_path: str) -> dict`: Returns {text, extracted_data}
- Supports image files and PDFs (via pdf2image)

### ExtractionService
Extracts structured data from raw text.
- `extract_structured_data(text: str, doc_type: str) -> dict`
- Handles receipt parsing, invoice extraction, general text

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql+asyncpg://localhost/voicedb |
| OPENAI_API_KEY | OpenAI API key for Whisper | None |
| UPLOAD_DIR | Directory for uploaded files | ./uploads |
| MAX_FILE_SIZE | Maximum upload size (MB) | 10 |

## Future Phases

1. **Real-time Voice**: WebSocket support for live transcription
2. **Multi-user**: User authentication and authorization
3. **Analytics**: Dashboard with charts and trends
4. **Integrations**: Bank API connections, accounting software
5. **AI Enhancement**: GPT-based data categorization and suggestions