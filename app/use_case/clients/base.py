import abc
from typing import Iterator

from app.domain.models import UnifiedHost


class BaseNormalizer(abc.ABC):
    @abc.abstractmethod
    def normalize(self):
        pass


class BaseClient(abc.ABC):
    
    @abc.abstractmethod
    def fetch_hosts(self) -> Iterator[UnifiedHost]:
        pass
    
    @abc.abstractmethod
    def get_normalizer(self) -> BaseNormalizer:
        pass
