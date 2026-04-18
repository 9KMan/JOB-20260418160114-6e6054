from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal


class TransactionBase(BaseModel):
    amount: Decimal
    category: str
    description: str
    date: date


class TransactionCreate(TransactionBase):
    entry_id: UUID


class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None


class TransactionResponse(TransactionBase):
    id: UUID
    entry_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionSummary(BaseModel):
    total_amount: Decimal
    transaction_count: int
    by_category: dict[str, Decimal]
    by_month: dict[str, Decimal]
