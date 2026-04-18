import uuid
from typing import Optional
from decimal import Decimal
from datetime import date
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.transaction import Transaction
from app.models.entry import Entry
from app.schemas.transaction import (
    TransactionCreate, TransactionResponse, TransactionUpdate, TransactionSummary
)

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new transaction."""
    # Verify entry exists
    result = await db.execute(select(Entry).where(Entry.id == transaction.entry_id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    db_transaction = Transaction(
        entry_id=transaction.entry_id,
        amount=transaction.amount,
        category=transaction.category,
        description=transaction.description,
        date=transaction.date
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=list[TransactionResponse])
async def list_transactions(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """List transactions with optional filters."""
    query = select(Transaction).offset(skip).limit(limit).order_by(Transaction.date.desc())

    if category:
        query = query.where(Transaction.category == category)
    if start_date:
        query = query.where(Transaction.date >= start_date)
    if end_date:
        query = query.where(Transaction.date <= end_date)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/summary", response_model=TransactionSummary)
async def get_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get transaction summary with totals and breakdowns."""
    query = select(Transaction)
    if start_date:
        query = query.where(Transaction.date >= start_date)
    if end_date:
        query = query.where(Transaction.date <= end_date)

    result = await db.execute(query)
    transactions = result.scalars().all()

    total_amount = sum(t.amount for t in transactions)
    transaction_count = len(transactions)

    # Group by category
    by_category = {}
    for t in transactions:
        by_category[t.category] = by_category.get(t.category, Decimal(0)) + t.amount

    # Group by month
    by_month = {}
    for t in transactions:
        month_key = t.date.strftime("%Y-%m")
        by_month[month_key] = by_month.get(month_key, Decimal(0)) + t.amount

    return TransactionSummary(
        total_amount=total_amount,
        transaction_count=transaction_count,
        by_category=by_category,
        by_month=by_month
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get transaction by ID."""
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: uuid.UUID,
    update: TransactionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update transaction."""
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if update.amount is not None:
        transaction.amount = update.amount
    if update.category is not None:
        transaction.category = update.category
    if update.description is not None:
        transaction.description = update.description
    if update.date is not None:
        transaction.date = update.date

    await db.commit()
    await db.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete transaction."""
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    await db.delete(transaction)
    await db.commit()
    return {"message": "Transaction deleted"}
