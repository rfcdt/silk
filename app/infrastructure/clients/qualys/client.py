from typing import Iterator, List

import requests

from app.domain.models import UnifiedHost
from app.infrastructure.clients.base import BaseClient

from .asset_merger import QualysAssetMerger
from .normalizer import QualysNormalizer


class QualysClient(BaseClient):
    API_URL = "https://api.recruiting.app.silk.security/api/qualys/hosts/get"
    TIMEOUT = 5

    def __init__(self, api_key: str, limit: int = 1, skip: int = 0):
        self.api_key = api_key
        self.limit = limit
        self.skip = skip

    def fetch_hosts(self) -> Iterator[List[UnifiedHost]]:
        """
        Yield raw host objects from Qualys API.
        """
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
        if response.status_code != 200:
            return None

        return response.json()

    def get_normalizer(self):
        return QualysNormalizer()

    def get_asset_merger(self):
        return QualysAssetMerger()
