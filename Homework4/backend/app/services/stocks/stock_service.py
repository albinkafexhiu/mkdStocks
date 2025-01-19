from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .repositories.stock_repository import StockRepository
from .builders.market_data_builder import MarketDataBuilder
from .builders.stock_data_builder import StockDataBuilder

class StockService:
    def __init__(self, db: Session):
        self.repository = StockRepository(db)
        self.market_builder = MarketDataBuilder()
        self.stock_builder = StockDataBuilder()

    def get_symbols(self) -> List[str]:
        return self.repository.get_symbols()

    def get_market_overview(self) -> List[Dict[str, Any]]:
        rows = self.repository.get_market_overview()
        return [
            self.market_builder
                .set_symbol(row[0])
                .set_prices(row[1], row[2])
                .set_volume(row[4], row[5])
                .set_date(row[6])
                .build()
            for row in rows
        ]

    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        rows = self.repository.get_stock_data(symbol, start_date, end_date)
        return [
            self.stock_builder
                .set_date_price(row[0], row[1])
                .set_price_range(row[2], row[3], row[4])
                .set_metrics(row[5], row[6], row[7], row[8])
                .build()
            for row in rows
        ]
    def get_popular_stocks(self) -> List[Dict[str, Any]]:
        rows = self.repository.get_popular_stocks()
        return [{
            "symbol": row[0],
            "companyName": row[0],  # Using symbol as company name for now
            "price": float(row[1]),
            "changePercentage": float(row[2]) if row[2] is not None else 0.0
        } for row in rows]

    def get_wishlist(self, db: Session) -> List[Dict[str, Any]]:
        rows = self.repository.get_wishlist()
        return [{
            "symbol": row[0],
            "companyName": row[0],  # Using symbol as company name for now
            "price": float(row[1]),
            "changePercentage": float(row[2]) if row[2] is not None else 0.0
        } for row in rows]    