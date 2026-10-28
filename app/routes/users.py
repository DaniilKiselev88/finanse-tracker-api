from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.db import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Проверяем email
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email and existing_email.is_active:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    # 2. Проверяем телефон (если передан)
    if user_data.phone:
        existing_phone = db.query(User).filter(User.phone == user_data.phone).first()
        if existing_phone:
            if existing_phone.is_active:
                raise HTTPException(status_code=400, detail="Телефон уже зарегистрирован")
            else:
                existing_phone.phone = None # Освобождаем старый

    # 3. Создаем пользователя
    new_user = User(
        email=user_data.email,
        phone=user_data.phone,
        hashed_password=hash_password(user_data.password),
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user