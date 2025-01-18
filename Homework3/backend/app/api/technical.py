from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from datetime import datetime
from typing import Optional, Dict, Any, List

import pandas as pd
import numpy as np
import ta  

router = APIRouter()

@router.get("/technical/{symbol}")
def get_technical_analysis(
    symbol: str,
    timeframe: str = Query("6M", description="Timeframe quick select (e.g., 1M, 3M, 6M, 1Y)"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Returns 10 technical indicators (5 oscillators, 5 MAs) plus a combined signal
    for daily, weekly, monthly data for the given symbol.
    'timeframe' is a quick selection: 1M, 3M, 6M, 1Y, etc. 
    """

    # 1) Convert timeframe into start_date
    end_date = pd.Timestamp.today().normalize()  # "today"
    if timeframe.upper() == "1M":
        start_date = end_date - pd.DateOffset(months=1)
    elif timeframe.upper() == "3M":
        start_date = end_date - pd.DateOffset(months=3)
    elif timeframe.upper() == "6M":
        start_date = end_date - pd.DateOffset(months=6)
    elif timeframe.upper() == "1Y":
        start_date = end_date - pd.DateOffset(years=1)
    else:
        # default 6M
        start_date = end_date - pd.DateOffset(months=6)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    # 2) Fetch daily data from the DB in [start_date, end_date]
    query = text("""
        SELECT date, last_trade_price, volume
        FROM stock_data
        WHERE symbol = :symbol
          AND date >= :start_date
          AND date <= :end_date
        ORDER BY date ASC
    """)
    rows = db.execute(query, {
        "symbol": symbol,
        "start_date": start_str,
        "end_date": end_str
    }).fetchall()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {symbol} in range {start_str} - {end_str}"
        )

    # 3) daily DataFrame
    df_daily = pd.DataFrame(rows, columns=["date", "close", "volume"])
    df_daily["date"] = pd.to_datetime(df_daily["date"])
    df_daily.set_index("date", inplace=True)

    def compute_indicators(df: pd.DataFrame, freq_label: str) -> pd.DataFrame:
        # Fill missing
        df["close"] = df["close"].ffill()
        df["volume"] = df["volume"].fillna(0)

        # 5 Oscillators
        df[f"rsi_{freq_label}"] = ta.momentum.rsi(df["close"], window=14, fillna=True)

        df[f"stoch_k_{freq_label}"] = ta.momentum.stoch(
            df["close"], df["close"], df["close"], window=14, smooth_window=3, fillna=True
        )
        df[f"stoch_d_{freq_label}"] = ta.momentum.stoch_signal(
            df["close"], df["close"], df["close"], window=14, smooth_window=3, fillna=True
        )

        df[f"williamsr_{freq_label}"] = ta.momentum.williams_r(
            df["close"], df["close"], df["close"], lbp=14, fillna=True
        )
        df[f"cci_{freq_label}"] = ta.trend.cci(
            df["close"], df["close"], df["close"], window=20, constant=0.015, fillna=True
        )
        df[f"mfi_{freq_label}"] = ta.volume.money_flow_index(
            df["close"], df["close"], df["close"], df["volume"], window=14, fillna=True
        )

        # 5 Moving Averages
        df[f"sma_{freq_label}"] = ta.trend.SMAIndicator(df["close"], window=20, fillna=True).sma_indicator()
        df[f"ema_{freq_label}"] = ta.trend.EMAIndicator(df["close"], window=20, fillna=True).ema_indicator()
        df[f"wma_{freq_label}"] = ta.trend.WMAIndicator(df["close"], window=20, fillna=True).wma()

        # We'll define a TEMA by 3 passes of EMA (a quick hack):
        ema1 = ta.trend.EMAIndicator(df["close"], window=20, fillna=True).ema_indicator()
        ema2 = ta.trend.EMAIndicator(ema1, window=20, fillna=True).ema_indicator()
        ema3 = ta.trend.EMAIndicator(ema2, window=20, fillna=True).ema_indicator()
        df[f"tema_{freq_label}"] = 3*ema1 - 3*ema2 + ema3

        # For the 5th MA let's do WEMA or a fallback
        try:
            wema = ta.trend.WEMAIndicator(df["close"], window=20, fillna=True).wema()
            df[f"wema_{freq_label}"] = wema
        except AttributeError:
            # fallback to same as EMA
            df[f"wema_{freq_label}"] = df[f"ema_{freq_label}"]

        # Add a final combined signal
        df[f"signal_{freq_label}"] = df.apply(lambda row: generate_combined_signal(row, freq_label), axis=1)

        return df

    def generate_combined_signal(row, freq_label: str) -> str:
        """
        Naive approach: Each of the 10 indicators 'votes' buy/sell/hold.
        Tally them up and return the majority.
        """
        votes = []
        # RSI
        rsi_val = row[f"rsi_{freq_label}"]
        votes.append("buy" if rsi_val < 30 else ("sell" if rsi_val > 70 else "hold"))

        # Stoch K
        stoch_k = row[f"stoch_k_{freq_label}"]
        votes.append("buy" if stoch_k < 20 else ("sell" if stoch_k > 80 else "hold"))

        # Williams
        w_val = row[f"williamsr_{freq_label}"]
        votes.append("buy" if w_val < -80 else ("sell" if w_val > -20 else "hold"))

        # CCI
        cci_val = row[f"cci_{freq_label}"]
        votes.append("buy" if cci_val < -100 else ("sell" if cci_val > 100 else "hold"))

        # MFI
        mfi_val = row[f"mfi_{freq_label}"]
        votes.append("buy" if mfi_val < 35 else ("sell" if mfi_val > 65 else "hold"))

        # For MAs, a simple approach: if close > MA => "buy", else if close < MA => "sell", else "hold"
        close_val = row["close"]

        # sma
        sma_val = row[f"sma_{freq_label}"]
        votes.append("buy" if close_val > sma_val else ("sell" if close_val < sma_val else "hold"))

        # ema
        ema_val = row[f"ema_{freq_label}"]
        votes.append("buy" if close_val > ema_val else ("sell" if close_val < ema_val else "hold"))

        # wma
        wma_val = row[f"wma_{freq_label}"]
        votes.append("buy" if close_val > wma_val else ("sell" if close_val < wma_val else "hold"))

        # wema
        wema_val = row[f"wema_{freq_label}"]
        votes.append("buy" if close_val > wema_val else ("sell" if close_val < wema_val else "hold"))

        # tema
        tema_val = row[f"tema_{freq_label}"]
        votes.append("buy" if close_val > tema_val else ("sell" if close_val < tema_val else "hold"))

        # Tally
        buy_count = votes.count("buy")
        sell_count = votes.count("sell")
        if buy_count > sell_count:
            return "BUY"
        elif sell_count > buy_count:
            return "SELL"
        else:
            return "HOLD"

    # 4) Compute for daily
    df_daily_ind = compute_indicators(df_daily.copy(), "daily")

    # 5) Weekly => resample
    df_weekly = df_daily.resample("W").last().dropna(subset=["close"])
    df_weekly_ind = compute_indicators(df_weekly.copy(), "weekly")

    # 6) Monthly => resample
    df_monthly = df_daily.resample("M").last().dropna(subset=["close"])
    df_monthly_ind = compute_indicators(df_monthly.copy(), "monthly")

    # Convert data to JSON
    def df_to_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
        df_reset = df.reset_index()
        df_reset["date"] = df_reset["date"].dt.strftime("%Y-%m-%d")
        return df_reset.to_dict(orient="records")

    daily_data = df_to_records(df_daily_ind)
    weekly_data = df_to_records(df_weekly_ind)
    monthly_data = df_to_records(df_monthly_ind)

    return {
        "symbol": symbol,
        "timeframe_selected": timeframe,
        "date_range": {"start": start_str, "end": end_str},
        "daily": daily_data,
        "weekly": weekly_data,
        "monthly": monthly_data
    }
