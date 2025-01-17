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
    
@router.get("/market-overview")
def get_market_overview(db: Session = Depends(get_db)):
    try:
        # Get data for the last 30 days
        query = text("""
            WITH LastTrades AS (
                -- Get the last trade for each symbol
                SELECT 
                    symbol,
                    last_trade_price as current_price,
                    volume as last_volume,
                    date as last_trade_date,
                    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) as rn
                FROM stock_data
                WHERE date >= CURRENT_DATE - INTERVAL '30 days'
            ),
            FirstTrades AS (
                -- Get the first trade in the period for each symbol
                SELECT 
                    symbol,
                    last_trade_price as start_price,
                    date as start_date,
                    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date ASC) as rn
                FROM stock_data
                WHERE date >= CURRENT_DATE - INTERVAL '30 days'
            ),
            VolumeStats AS (
                -- Calculate total volume and turnover for the period
                SELECT 
                    symbol,
                    SUM(volume) as total_volume,
                    SUM(volume * last_trade_price) as total_turnover
                FROM stock_data
                WHERE date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY symbol
            )
            SELECT 
                lt.symbol,
                lt.current_price,
                ft.start_price,
                ((lt.current_price - ft.start_price) / ft.start_price * 100) as price_change,
                vs.total_volume,
                vs.total_turnover,
                lt.last_trade_date
            FROM LastTrades lt
            JOIN FirstTrades ft ON lt.symbol = ft.symbol AND lt.rn = 1 AND ft.rn = 1
            JOIN VolumeStats vs ON lt.symbol = vs.symbol
            WHERE lt.current_price > 0 AND ft.start_price > 0
            ORDER BY price_change DESC
        """)
        
        result = db.execute(query)
        
        data = [{
            "symbol": row[0],
            "currentPrice": float(row[1]),
            "startPrice": float(row[2]),
            "priceChange": float(row[3]),
            "totalVolume": int(row[4]),
            "totalTurnover": float(row[5]),
            "lastTradeDate": row[6].strftime("%Y-%m-%d")
        } for row in result]
        
        return data
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