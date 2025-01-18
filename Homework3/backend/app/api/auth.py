from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from typing import Dict

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(
        status_code=200,
        content={"message": "User created successfully"}
    )

@router.post("/login")
async def login(credentials: Dict[str, str], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials["email"]).first()
    if not user or user.password != credentials["password"]:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return JSONResponse(
        status_code=200,
        content={"message": "Login successful"}
    )