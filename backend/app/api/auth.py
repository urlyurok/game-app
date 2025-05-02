from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    db_user = db.query(User).filter(User.nickname == user.nickname).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Никнейм уже занят")

    hashed_password = get_password_hash(user.password)
    db_user = User(nickname=user.nickname, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": user.nickname})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Авторизация пользователя"""
    db_user = db.query(User).filter(User.nickname == user.nickname).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=401, detail="Неверный никнейм или пароль")

    access_token = create_access_token(data={"sub": user.nickname})
    return {"access_token": access_token, "token_type": "bearer"}
