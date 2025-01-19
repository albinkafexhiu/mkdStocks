from abc import ABC, abstractmethod
from typing import Any, Optional

class NewsProcessor(ABC):
    def __init__(self):
        self._next_processor: Optional[NewsProcessor] = None

    def set_next(self, processor: 'NewsProcessor') -> 'NewsProcessor':
        self._next_processor = processor
        return processor

    def process_next(self, data: Any) -> Any:
        if self._next_processor:
            return self._next_processor.process(data)
        return data

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass