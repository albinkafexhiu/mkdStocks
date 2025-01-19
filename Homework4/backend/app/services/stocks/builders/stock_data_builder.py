from datetime import datetime
from typing import Dict, Any

class StockDataBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.data = {}

    def set_date_price(self, date: datetime, price: float):
        self.data.update({
            "date": date.strftime("%Y-%m-%d"),
            "lastTradePrice": float(price)
        })
        return self

    def set_price_range(self, max_price: float, min_price: float, avg_price: float):
        self.data.update({
            "maxPrice": float(max_price),
            "minPrice": float(min_price),
            "avgPrice": float(avg_price)
        })
        return self

    def set_metrics(self, change_percentage: float, volume: int, turnover_best: float, total_turnover: float):
        self.data.update({
            "changePercentage": float(change_percentage),
            "volume": int(volume),
            "turnoverBest": float(turnover_best),
            "totalTurnover": float(total_turnover)
        })
        return self

    def build(self) -> Dict[str, Any]:
        result = self.data.copy()
        self.reset()
        return result