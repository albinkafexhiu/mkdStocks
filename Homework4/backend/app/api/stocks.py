from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.stocks.stock_service import StockService
from app.models.stock import WishlistItem
from typing import List, Dict, Any

router = APIRouter()

@router.get("/symbols")
def get_symbols(db: Session = Depends(get_db)):
    try:
        service = StockService(db)
        return service.get_symbols()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-overview")
def get_market_overview(db: Session = Depends(get_db)):
    try:
        service = StockService(db)
        return service.get_market_overview()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/popular-stocks")
def get_popular_stocks(db: Session = Depends(get_db)):
    try:
        service = StockService(db)
        return service.get_popular_stocks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/{symbol}")
def get_stock_data(
    symbol: str, 
    start_date: str, 
    end_date: str, 
    db: Session = Depends(get_db)
):
    try:
        service = StockService(db)
        return service.get_stock_data(symbol, start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/wishlist/{symbol}")
def add_to_wishlist(symbol: str, db: Session = Depends(get_db)):
    try:
        # Check if already exists
        existing = db.query(WishlistItem).filter(WishlistItem.symbol == symbol).first()
        if existing:
            raise HTTPException(status_code=400, detail="Symbol already in wishlist")
            
        wishlist_item = WishlistItem(symbol=symbol)
        db.add(wishlist_item)
        db.commit()
        return {"message": "Added to wishlist"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/wishlist/{symbol}")
def remove_from_wishlist(symbol: str, db: Session = Depends(get_db)):
    try:
        db.query(WishlistItem).filter(WishlistItem.symbol == symbol).delete()
        db.commit()
        return {"message": "Removed from wishlist"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/wishlist")
def get_wishlist(db: Session = Depends(get_db)):
    try:
        service = StockService(db)
        return service.get_wishlist(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))