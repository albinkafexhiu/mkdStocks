from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserBase
from typing import Dict

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        password=user.password,
        is_active=True
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return JSONResponse(
            status_code=200,
            content={"message": "User created successfully"}
        )
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating user")

@router.post("/login")
async def login(credentials: Dict[str, str], db: Session = Depends(get_db)):
    try:
        # Add logging to see what credentials are being received
        print(f"Login attempt with email: {credentials.get('email')}")
        
        user = db.query(User).filter(User.email == credentials.get('email')).first()
        
        if not user:
            print(f"No user found with email: {credentials.get('email')}")
            raise HTTPException(status_code=400, detail="Incorrect email or password")
            
        if user.password != credentials.get('password'):
            print(f"Invalid password for user: {credentials.get('email')}")
            raise HTTPException(status_code=400, detail="Incorrect email or password")
            
        if not user.is_active:
            raise HTTPException(status_code=400, detail="User is not active")
            
        return JSONResponse(
            status_code=200,
            content={"message": "Login successful"}
        )
    except Exception as e:
        print(f"Login error: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")