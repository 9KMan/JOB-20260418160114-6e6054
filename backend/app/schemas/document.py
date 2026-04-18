from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.document import DocumentStatus


class DocumentBase(BaseModel):
    filename: str


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    ocr_text: Optional[str] = None
    extracted_data: Optional[dict] = None
    status: Optional[DocumentStatus] = None


class DocumentResponse(DocumentBase):
    id: UUID
    file_path: str
    ocr_text: Optional[str] = None
    extracted_data: dict = Field(default_factory=dict)
    status: DocumentStatus
    created_at: datetime

    class Config:
        from_attributes = True
