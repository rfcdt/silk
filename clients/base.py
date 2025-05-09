import abc
from typing import Iterator

from models.host import UnifiedHostAsset


class BaseNormalizer(abc.ABC):
    @abc.abstractmethod
    def normalize(self):
        pass


class BaseClient(abc.ABC):
    
    @abc.abstractmethod
    def fetch_hosts(self) -> Iterator[UnifiedHostAsset]:
        pass
    
    @abc.abstractmethod
    def get_normalizer(self) -> BaseNormalizer:
        pass
