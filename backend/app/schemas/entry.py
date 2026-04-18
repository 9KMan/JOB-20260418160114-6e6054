from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.entry import EntryType


class EntryBase(BaseModel):
    type: EntryType
    content: str


class EntryCreate(EntryBase):
    source_document_id: Optional[UUID] = None
    metadata: dict = {}


class EntryUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[dict] = None


class EntryResponse(EntryBase):
    id: UUID
    source_document_id: Optional[UUID] = None
    metadata: dict
    created_at: datetime

    class Config:
        from_attributes = True
