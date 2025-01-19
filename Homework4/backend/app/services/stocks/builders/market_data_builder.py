from datetime import datetime
from typing import List, Dict, Any

class MarketDataBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.data = {}

    def set_symbol(self, symbol: str):
        self.data["symbol"] = symbol
        return self

    def set_prices(self, current_price: float, start_price: float):
        self.data.update({
            "currentPrice": float(current_price),
            "startPrice": float(start_price),
            "priceChange": float(((current_price - start_price) / start_price * 100))
        })
        return self

    def set_volume(self, volume: int, turnover: float):
        self.data.update({
            "totalVolume": int(volume),
            "totalTurnover": float(turnover)
        })
        return self

    def set_date(self, date: datetime):
        self.data["lastTradeDate"] = date.strftime("%Y-%m-%d")
        return self

    def build(self) -> Dict[str, Any]:
        result = self.data.copy()
        self.reset()
        return result