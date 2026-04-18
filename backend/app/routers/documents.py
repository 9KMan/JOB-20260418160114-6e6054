import os
import shutil
import tempfile
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentResponse, DocumentUpdate
from app.services.ocr_service import ocr_service
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/documents", tags=["documents"])

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a document and process with OCR.

    Accepts: images (jpg, png), PDFs, Word docs
    """
    # Generate unique filename
    ext = os.path.splitext(file.filename or "document")[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create document record
    doc = Document(
        filename=file.filename or "unknown",
        file_path=file_path,
        status=DocumentStatus.PENDING
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    # Process in background (for MVP, synchronously)
    try:
        doc.status = DocumentStatus.PROCESSING
        await db.commit()

        result = await ocr_service.process_document(file_path)
        doc.ocr_text = result["text"]
        doc.extracted_data = result["extracted_data"]
        doc.status = DocumentStatus.COMPLETED
    except Exception as e:
        doc.status = DocumentStatus.FAILED
        doc.extracted_data = {"error": str(e)}

    await db.commit()
    await db.refresh(doc)

    return doc


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all documents."""
    result = await db.execute(
        select(Document).offset(skip).limit(limit).order_by(Document.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get document by ID."""
    result = await db.execute(select(Document).where(Document.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: uuid.UUID,
    update: DocumentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update document (OCR text, extracted data, status)."""
    result = await db.execute(select(Document).where(Document.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if update.ocr_text is not None:
        doc.ocr_text = update.ocr_text
    if update.extracted_data is not None:
        doc.extracted_data = update.extracted_data
    if update.status is not None:
        doc.status = update.status

    await db.commit()
    await db.refresh(doc)
    return doc


@router.delete("/{document_id}")
async def delete_document(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete document and file."""
    result = await db.execute(select(Document).where(Document.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file
    if os.path.exists(doc.file_path):
        os.unlink(doc.file_path)

    await db.delete(doc)
    await db.commit()
    return {"message": "Document deleted"}
