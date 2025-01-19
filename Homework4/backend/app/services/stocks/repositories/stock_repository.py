from sqlalchemy import text
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .base_repository import BaseRepository

class StockRepository(BaseRepository):
    def get_symbols(self) -> List[str]:
        query = text("SELECT DISTINCT symbol FROM stock_data ORDER BY symbol")
        result = self.execute_query(query)
        return [row[0] for row in result]

    def get_market_overview(self) -> List[Dict[str, Any]]:
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
        return self.execute_query(query)

    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
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
        return self.execute_query(query, {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date
        })
        
    def get_popular_stocks(self) -> List[Dict[str, Any]]:
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
        return self.execute_query(query)

    def get_wishlist(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT DISTINCT ON (s.symbol)
                s.symbol,
                s.last_trade_price,
                s.change_percentage
            FROM stock_data s
            JOIN wishlist w ON s.symbol = w.symbol
            ORDER BY s.symbol, s.date DESC
        """)
        return self.execute_query(query) 