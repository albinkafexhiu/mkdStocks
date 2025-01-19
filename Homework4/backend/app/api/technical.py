from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from datetime import datetime
from typing import Optional, Dict, Any, List
import pandas as pd
from app.services.technical.technical_analyzer import TechnicalAnalyzer

router = APIRouter()

@router.get("/technical/{symbol}")
def get_technical_analysis(
    symbol: str,
    timeframe: str = Query("6M", description="Timeframe quick select (e.g., 1M, 3M, 6M, 1Y)"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Convert timeframe to date range
    end_date = pd.Timestamp.today().normalize()
    timeframe_map = {
        "1M": pd.DateOffset(months=1),
        "3M": pd.DateOffset(months=3),
        "6M": pd.DateOffset(months=6),
        "1Y": pd.DateOffset(years=1)
    }
    start_date = end_date - timeframe_map.get(timeframe.upper(), pd.DateOffset(months=6))
    
    # Fetch data from database
    query = text("""
        SELECT date, last_trade_price as close, volume
        FROM stock_data
        WHERE symbol = :symbol
          AND date >= :start_date
          AND date <= :end_date
        ORDER BY date ASC
    """)
    
    rows = db.execute(query, {
        "symbol": symbol,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }).fetchall()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {symbol} in specified timeframe"
        )

    # Create DataFrame
    df = pd.DataFrame(rows, columns=["date", "close", "volume"])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    # Initialize technical analyzer
    analyzer = TechnicalAnalyzer()
    
    # Perform analysis for all timeframes
    results = analyzer.analyze_data(df)
    
    # Convert results to response format
    def prepare_response_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
        df_reset = df.reset_index()
        df_reset["date"] = df_reset["date"].dt.strftime("%Y-%m-%d")
        return df_reset.to_dict(orient="records")

    response = {
        "symbol": symbol,
        "timeframe_selected": timeframe,
        "date_range": {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d")
        },
        "daily": prepare_response_data(results["daily"]),
        "weekly": prepare_response_data(results["weekly"]),
        "monthly": prepare_response_data(results["monthly"])
    }

    return response

@router.get("/indicator-settings")
def get_indicator_settings() -> Dict[str, Any]:
    """Get default settings for all technical indicators"""
    return {
        "oscillators": {
            "rsi": {
                "period": 14,
                "overbought": 70,
                "oversold": 30
            },
            "stochastic": {
                "k_period": 14,
                "d_period": 3,
                "overbought": 80,
                "oversold": 20
            },
            "williams_r": {
                "period": 14,
                "overbought": -20,
                "oversold": -80
            },
            "cci": {
                "period": 20,
                "constant": 0.015,
                "overbought": 100,
                "oversold": -100
            },
            "mfi": {
                "period": 14,
                "overbought": 80,
                "oversold": 20
            }
        },
        "moving_averages": {
            "sma": {
                "period": 20
            },
            "ema": {
                "period": 20
            },
            "wma": {
                "period": 20
            },
            "tema": {
                "period": 20
            },
            "wema": {
                "period": 20
            }
        }
    }