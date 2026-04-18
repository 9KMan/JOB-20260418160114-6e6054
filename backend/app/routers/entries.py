import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.entry import Entry, EntryType
from app.schemas.entry import EntryCreate, EntryResponse, EntryUpdate

router = APIRouter(prefix="/api/entries", tags=["entries"])


@router.post("/", response_model=EntryResponse)
async def create_entry(entry: EntryCreate, db: AsyncSession = Depends(get_db)):
    """Create a new entry (text, voice, or document source)."""
    db_entry = Entry(
        type=entry.type,
        content=entry.content,
        source_document_id=entry.source_document_id,
        metadata=entry.metadata
    )
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry


@router.get("/", response_model=list[EntryResponse])
async def list_entries(
    skip: int = 0,
    limit: int = 100,
    entry_type: Optional[EntryType] = None,
    db: AsyncSession = Depends(get_db)
):
    """List entries with optional type filter."""
    query = select(Entry).offset(skip).limit(limit).order_by(Entry.created_at.desc())
    if entry_type:
        query = query.where(Entry.type == entry_type)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{entry_id}", response_model=EntryResponse)
async def get_entry(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get entry by ID."""
    result = await db.execute(select(Entry).where(Entry.id == entry_id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.put("/{entry_id}", response_model=EntryResponse)
async def update_entry(
    entry_id: uuid.UUID,
    update: EntryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update entry content or metadata."""
    result = await db.execute(select(Entry).where(Entry.id == entry_id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    if update.content is not None:
        entry.content = update.content
    if update.metadata is not None:
        entry.metadata = update.metadata

    await db.commit()
    await db.refresh(entry)
    return entry


@router.delete("/{entry_id}")
async def delete_entry(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete entry."""
    result = await db.execute(select(Entry).where(Entry.id == entry_id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    await db.delete(entry)
    await db.commit()
    return {"message": "Entry deleted"}
