from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class TransactionCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Сумма должна быть больше 0")
    type: str = Field(..., pattern="^(income|expense)$", description="Только 'income' или 'expense'")
    category: Optional[str] = None
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    type: str
    category: Optional[str]
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True