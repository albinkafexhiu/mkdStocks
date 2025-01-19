import pandas as pd
import ta
from .base_strategy import BaseStrategy
from typing import Dict, Any

class SMAStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.window = self.params.get('window', 20)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        return ta.trend.sma_indicator(data['close'], window=self.window)

    def generate_signal(self, value: float, price: float) -> str:
        if price > value:
            return "BUY"
        elif price < value:
            return "SELL"
        return "HOLD"

class EMAStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.window = self.params.get('window', 20)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        return ta.trend.ema_indicator(data['close'], window=self.window)

    def generate_signal(self, value: float, price: float) -> str:
        if price > value:
            return "BUY"
        elif price < value:
            return "SELL"
        return "HOLD"

class WMAStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.window = self.params.get('window', 20)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        return ta.trend.wma_indicator(data['close'], window=self.window)

    def generate_signal(self, value: float, price: float) -> str:
        if price > value:
            return "BUY"
        elif price < value:
            return "SELL"
        return "HOLD"

class TEMAStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.window = self.params.get('window', 20)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        ema1 = ta.trend.ema_indicator(data['close'], window=self.window)
        ema2 = ta.trend.ema_indicator(ema1, window=self.window)
        ema3 = ta.trend.ema_indicator(ema2, window=self.window)
        return 3 * ema1 - 3 * ema2 + ema3

    def generate_signal(self, value: float, price: float) -> str:
        if price > value:
            return "BUY"
        elif price < value:
            return "SELL"
        return "HOLD"

class WEMAStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.window = self.params.get('window', 20)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        try:
            return ta.trend.wema_indicator(data['close'], window=self.window)
        except AttributeError:
            # Fallback to EMA if WEMA is not available
            return ta.trend.ema_indicator(data['close'], window=self.window)

    def generate_signal(self, value: float, price: float) -> str:
        if price > value:
            return "BUY"
        elif price < value:
            return "SELL"
        return "HOLD"