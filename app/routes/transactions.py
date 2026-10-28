from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.db import SessionLocal
from app.models.transactions import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.core.deps import get_current_user
from app.core.ml_classifier import predict_category

router = APIRouter(prefix="/transactions", tags=["transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    trans_data: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    final_category = trans_data.category
    if not final_category or final_category == "Разное":
        final_category = predict_category(trans_data.description)

    new_trans = Transaction(
        user_id=current_user.id, 
        amount=trans_data.amount,
        type=trans_data.type,
        category=final_category,
        description=trans_data.description
    )
    db.add(new_trans)
    db.commit()
    db.refresh(new_trans)
    return new_trans

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).all()

@router.delete("/{trans_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    trans_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trans = db.query(Transaction).filter(
        Transaction.id == trans_id, 
        Transaction.user_id == current_user.id
    ).first()
    
    if not trans:
        raise HTTPException(status_code=404, detail="Транзакция не найдена или не принадлежит вам")
    
    db.delete(trans)
    db.commit()
    return None