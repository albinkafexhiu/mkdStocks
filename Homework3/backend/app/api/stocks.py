from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from typing import List
from datetime import datetime
from app.models.stock import WishlistItem

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
        query = text("""
            WITH LastTrades AS (
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
                SELECT 
                    symbol,
                    last_trade_price as start_price,
                    date as start_date,
                    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date ASC) as rn
                FROM stock_data
                WHERE date >= CURRENT_DATE - INTERVAL '30 days'
            ),
            VolumeStats AS (
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

@router.get("/popular-stocks")
def get_popular_stocks(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT DISTINCT ON (s.symbol)
                s.symbol,
                s.last_trade_price,
                s.change_percentage,
                s.date
            FROM stock_data s
            ORDER BY s.symbol, s.date DESC
            LIMIT 6
        """)
        
        result = db.execute(query)
        stocks = [{
            "symbol": row[0],
            "companyName": row[0],  # Using symbol as company name for now
            "price": float(row[1]),
            "changePercentage": float(row[2]) if row[2] is not None else 0.0
        } for row in result]
        
        return stocks
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
        query = text("""
            SELECT DISTINCT ON (s.symbol)
                s.symbol,
                s.last_trade_price,
                s.change_percentage
            FROM stock_data s
            JOIN wishlist w ON s.symbol = w.symbol
            ORDER BY s.symbol, s.date DESC
        """)
        
        result = db.execute(query)
        stocks = [{
            "symbol": row[0],
            "companyName": row[0],  # Using symbol as company name for now
            "price": float(row[1]),
            "changePercentage": float(row[2]) if row[2] is not None else 0.0
        } for row in result]
        
        return stocks
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
    
@router.get("/technical-analysis/{symbol}")
def get_technical_analysis(symbol: str,
                          start_date: str,
                          end_date: str,
                          db: Session = Depends(get_db)):
    # 1) Query DB
    query = text("""
        SELECT date, last_trade_price, volume
        FROM stock_data
        WHERE symbol = :symbol
          AND date BETWEEN :start_date AND :end_date
        ORDER BY date ASC
    """)
    rows = db.execute(query, {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date
    }).fetchall()

    # 2) DataFrame
    df = pd.DataFrame(rows, columns=["date", "close", "volume"])
    if df.empty:
        return {"data": [], "message": "No data for this symbol in the given range."}

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # 3) Calculate indicators (just an example for RSI & SMA)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)

    # 4) Basic signals
    def rsi_signal(rsi_val: float) -> str:
        if rsi_val < 30:
            return "Buy"
        elif rsi_val > 70:
            return "Sell"
        else:
            return "Hold"
    df['rsi_signal'] = df['rsi'].apply(rsi_signal)

    # 5) Convert to JSON
    data = df.reset_index().to_dict(orient='records')
    return {"data": data}
