from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class BaseStrategy(ABC):
    def __init__(self, params: Dict[str, Any] = None):
        self.params = params or {}

    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """Calculate the indicator value"""
        pass

    @abstractmethod
    def generate_signal(self, value: float) -> str:
        """Generate trading signal based on indicator value"""
        pass