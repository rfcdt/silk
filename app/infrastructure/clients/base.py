import abc
from typing import Iterator

import requests

from app.domain.models import UnifiedHost


class AssetMerger(abc.ABC):
    @abc.abstractmethod
    def merge(self, source_data: UnifiedHost, existing: UnifiedHost):
        pass


class BaseNormalizer(abc.ABC):
    @abc.abstractmethod
    def normalize(self, raw: dict):
        pass


class BaseClient(abc.ABC):
    
    @abc.abstractmethod
    def fetch_hosts(self) -> Iterator[list[UnifiedHost]]:
        pass
    
    @abc.abstractmethod
    def get_normalizer(self) -> BaseNormalizer:
        pass

    @abc.abstractmethod
    def get_asset_merger(self) -> AssetMerger:
        pass


class SimpleBaseClient(BaseClient, abc.ABC):
    API_URL = ""
    TIMEOUT = 5
    skip = 0
    limit = 1

    HTTP_OK = 200
    HTTP_NOT_FOUND = 404

    def fetch_hosts(self) -> Iterator[list[UnifiedHost]]:
        """Yield raw host objects from Qualys API."""
        normalizer = self.get_normalizer()
        while True:
            response = self._fetch_page()
            if not response:
                break

            result = [normalizer.normalize(host) for host in response]
            yield result

            self.skip += self.limit

    def _fetch_page(self) -> list[UnifiedHost]:
        response = requests.post(
            f"{self.API_URL}?skip={self.skip}&limit={self.limit}",
            headers={
                "Accept": "application/json",
                "token": self.api_key,
            },
            timeout=self.TIMEOUT,
        )
        
        if response.status_code == self.HTTP_NOT_FOUND:
            raise Exception('Error happened. Check API key.')

        if response.status_code != self.HTTP_OK:
            return None

        return response.json()
