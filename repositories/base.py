from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class AbstractMongoRepository(ABC):
    @abstractmethod
    def find_all(self, collection: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def find_by_filter(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def save_one(self, collection: str, document: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def update_one(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> Any:
        pass
