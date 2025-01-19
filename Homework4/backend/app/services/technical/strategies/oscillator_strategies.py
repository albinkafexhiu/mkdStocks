import pandas as pd
import ta
from .base_strategy import BaseStrategy
from typing import Dict, Any

class RSIStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.period = self.params.get('period', 14)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        return ta.momentum.rsi(data['close'], window=self.period, fillna=True)

    def generate_signal(self, value: float) -> str:
        if value < 30:
            return "BUY"
        elif value > 70:
            return "SELL"
        return "HOLD"

class StochasticStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.window = self.params.get('window', 14)
        self.smooth_window = self.params.get('smooth_window', 3)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        stoch_k = ta.momentum.stoch(
            data['close'], data['close'], data['close'],
            window=self.window, smooth_window=self.smooth_window,
            fillna=True
        )
        stoch_d = ta.momentum.stoch_signal(
            data['close'], data['close'], data['close'],
            window=self.window, smooth_window=self.smooth_window,
            fillna=True
        )
        return pd.DataFrame({'stoch_k': stoch_k, 'stoch_d': stoch_d})

    def generate_signal(self, value: Dict[str, float]) -> str:
        k_value = value['stoch_k']
        if k_value < 20:
            return "BUY"
        elif k_value > 80:
            return "SELL"
        return "HOLD"

class WilliamsRStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.period = self.params.get('period', 14)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        return ta.momentum.williams_r(
            data['close'], data['close'], data['close'], 
            lbp=self.period,
            fillna=True
        )

    def generate_signal(self, value: float) -> str:
        if value < -80:
            return "BUY"
        elif value > -20:
            return "SELL"
        return "HOLD"

class CCIStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.window = self.params.get('window', 20)
        self.constant = self.params.get('constant', 0.015)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        return ta.trend.cci(
            data['close'], data['close'], data['close'],
            window=self.window, constant=self.constant
        )

    def generate_signal(self, value: float) -> str:
        if value < -100:
            return "BUY"
        elif value > 100:
            return "SELL"
        return "HOLD"

class MFIStrategy(BaseStrategy):
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.period = self.params.get('period', 14)

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        return ta.volume.money_flow_index(
            data['close'], data['close'], data['close'],
            data['volume'], window=self.period
        )

    def generate_signal(self, value: float) -> str:
        if value < 20:
            return "BUY"
        elif value > 80:
            return "SELL"
        return "HOLD"