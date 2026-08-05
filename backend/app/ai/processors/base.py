from abc import ABC, abstractmethod
from typing import List, Dict


class BaseProcessor(ABC):
    @abstractmethod
    async def process(self, signals: List[Dict]) -> List[Dict]:
        ...
