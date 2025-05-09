from typing import Iterator

import requests

from app.domain.models import UnifiedHost
from app.infrastructure.clients.base import BaseClient

from .asset_merger import CrowdstrikeAssetMerger
from .normalizer import CrowdstrikeNormalizer


class CrowdstrikeClient(BaseClient):
    API_URL = "https://api.recruiting.app.silk.security/api/crowdstrike/hosts/get"
    TIMEOUT = 5

    def __init__(
        self, api_key: str, limit: int = 2, skip: int = 0
    ):  # TODO:: check limit: sometime 2 and 1 response
        self.api_key = api_key
        self.limit = limit
        self.skip = skip

    def fetch_hosts(self) -> Iterator[UnifiedHost]:
        """
        Yield raw host objects from Qualys API.
        """
        normalizer = self.get_normalizer()
        while True:
            response = self._fetch_page()
            if not response:
                break

            for host in response:
                result = normalizer.normalize(host)
                yield result
            break

        self.skip += self.limit

    def _fetch_page(self) -> list[dict] | None:
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
        return CrowdstrikeNormalizer()

    def get_asset_merger(self):
        return CrowdstrikeAssetMerger()
