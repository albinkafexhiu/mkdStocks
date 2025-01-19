import pandas as pd
from typing import Dict, Any, List
from .indicator_factory import IndicatorFactory
from .strategies.base_strategy import BaseStrategy

class TechnicalAnalyzer:
    def __init__(self):
        self.factory = IndicatorFactory()
        
    def analyze_timeframe(self, data: pd.DataFrame, freq_label: str) -> pd.DataFrame:
        """Analyze data for a specific timeframe"""
        # Get all indicators
        indicators = self.factory.get_all_indicators()
        
        # Calculate each indicator
        for name, indicator in indicators.items():
            result = indicator.calculate(data)
            
            if isinstance(result, pd.DataFrame):  # For Stochastic
                for col in result.columns:
                    data[f"{col}_{freq_label}"] = result[col]
            else:
                data[f"{name}_{freq_label}"] = result

        # Generate signals
        data[f"signal_{freq_label}"] = data.apply(
            lambda row: self.combine_signals(row, freq_label, indicators), 
            axis=1
        )
        
        return data

    def combine_signals(self, row: pd.Series, freq_label: str, indicators: Dict[str, BaseStrategy]) -> str:
        """Combine signals from all indicators"""
        votes = []
        price = row['close']
        
        # Get signals from oscillators
        for name, indicator in indicators.items():
            if name == 'stochastic':
                value = {'stoch_k': row[f"stoch_k_{freq_label}"], 
                        'stoch_d': row[f"stoch_d_{freq_label}"]}
            else:
                value = row.get(f"{name}_{freq_label}")
                
            if value is not None:
                if name in ['sma', 'ema', 'wma', 'tema', 'wema']:
                    votes.append(indicator.generate_signal(value, price))
                else:
                    votes.append(indicator.generate_signal(value))

        # Count votes
        buy_count = votes.count("BUY")
        sell_count = votes.count("SELL")
        
        if buy_count > sell_count:
            return "BUY"
        elif sell_count > buy_count:
            return "SELL"
        return "HOLD"

    def analyze_data(self, data: pd.DataFrame, timeframes: List[str] = None) -> Dict[str, pd.DataFrame]:
        """Analyze data for all timeframes"""
        if timeframes is None:
            timeframes = ['daily', 'weekly', 'monthly']
            
        results = {}
        
        # Daily analysis (original data)
        daily_data = data.copy()
        results['daily'] = self.analyze_timeframe(daily_data, 'daily')
        
        # Weekly analysis
        if 'weekly' in timeframes:
            weekly_data = data.resample('W').last().dropna(subset=['close'])
            results['weekly'] = self.analyze_timeframe(weekly_data, 'weekly')
            
        # Monthly analysis
        if 'monthly' in timeframes:
            monthly_data = data.resample('M').last().dropna(subset=['close'])
            results['monthly'] = self.analyze_timeframe(monthly_data, 'monthly')
            
        return results