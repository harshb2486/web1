from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseProvider(ABC):
    @abstractmethod
    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        ...

    async def health_check(self) -> bool:
        return True
