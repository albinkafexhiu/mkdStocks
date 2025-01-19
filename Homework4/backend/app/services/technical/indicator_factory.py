from typing import Dict, Any
from .strategies.oscillator_strategies import (
    RSIStrategy, StochasticStrategy, WilliamsRStrategy, 
    CCIStrategy, MFIStrategy
)
from .strategies.moving_average_strategies import (
    SMAStrategy, EMAStrategy, WMAStrategy, 
    TEMAStrategy, WEMAStrategy
)
from .strategies.base_strategy import BaseStrategy


class IndicatorFactory:
    @staticmethod
    def create_oscillator(name: str, params: Dict[str, Any] = None) -> BaseStrategy:
        oscillators = {
            'rsi': RSIStrategy,
            'stochastic': StochasticStrategy,
            'williams_r': WilliamsRStrategy,
            'cci': CCIStrategy,
            'mfi': MFIStrategy
        }
        strategy_class = oscillators.get(name.lower())
        if not strategy_class:
            raise ValueError(f"Unsupported oscillator: {name}")
        return strategy_class(params)

    @staticmethod
    def create_moving_average(name: str, params: Dict[str, Any] = None) -> BaseStrategy:
        moving_averages = {
            'sma': SMAStrategy,
            'ema': EMAStrategy,
            'wma': WMAStrategy,
            'tema': TEMAStrategy,
            'wema': WEMAStrategy
        }
        strategy_class = moving_averages.get(name.lower())
        if not strategy_class:
            raise ValueError(f"Unsupported moving average: {name}")
        return strategy_class(params)

    @staticmethod
    def get_all_indicators(params: Dict[str, Any] = None) -> Dict[str, BaseStrategy]:
        indicators = {}
        # Add oscillators
        indicators['rsi'] = RSIStrategy(params)
        indicators['stochastic'] = StochasticStrategy(params)
        indicators['williams_r'] = WilliamsRStrategy(params)
        indicators['cci'] = CCIStrategy(params)
        indicators['mfi'] = MFIStrategy(params)
        # Add moving averages
        indicators['sma'] = SMAStrategy(params)
        indicators['ema'] = EMAStrategy(params)
        indicators['wma'] = WMAStrategy(params)
        indicators['tema'] = TEMAStrategy(params)
        indicators['wema'] = WEMAStrategy(params)
        return indicators