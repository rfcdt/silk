import abc
from typing import Iterator

from app.domain.models import UnifiedHost


class AssetMerger(abc.ABC):
    @abc.abstractmethod
    def merge(self, source_data: dict, existing: UnifiedHost):
        pass


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

    @abc.abstractmethod
    def get_asset_merger(self) -> AssetMerger:
        pass
    