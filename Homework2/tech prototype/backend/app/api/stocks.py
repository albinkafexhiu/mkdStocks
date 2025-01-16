from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/symbols")
def get_symbols(db: Session = Depends(get_db)):
    try:
        query = text("SELECT DISTINCT symbol FROM stock_data ORDER BY symbol")
        result = db.execute(query)
        symbols = [row[0] for row in result]
        return symbols
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
        query = text("""
            SELECT 
                date,
                last_trade_price,
                max_price,
                min_price,
                avg_price,
                change_percentage,
                volume,
                turnover_best,
                total_turnover
            FROM stock_data
            WHERE symbol = :symbol
            AND date BETWEEN :start_date AND :end_date
            ORDER BY date
        """)
        
        result = db.execute(query, {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date
        })
        
        data = [{
            "date": row[0].strftime("%Y-%m-%d"),
            "lastTradePrice": float(row[1]),
            "maxPrice": float(row[2]),
            "minPrice": float(row[3]),
            "avgPrice": float(row[4]),
            "changePercentage": float(row[5]),
            "volume": int(row[6]),
            "turnoverBest": float(row[7]),
            "totalTurnover": float(row[8])
        } for row in result]
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))