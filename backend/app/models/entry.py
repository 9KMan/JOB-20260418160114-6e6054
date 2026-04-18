import uuid
from datetime import datetime
from sqlalchemy import String, Text, Enum as SQLEnum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class EntryType(str, enum.Enum):
    TEXT = "text"
    VOICE = "voice"
    DOCUMENT = "document"


class Entry(Base):
    __tablename__ = "entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[EntryType] = mapped_column(SQLEnum(EntryType), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True
    )
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    source_document: Mapped["Document"] = relationship("Document", back_populates="entries")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="entry")


from app.models.document import Document
from app.models.transaction import Transaction
