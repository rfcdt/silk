from app.infrastructure.clients.base import SimpleBaseClient

from .asset_merger import CrowdstrikeAssetMerger
from .normalizer import CrowdstrikeNormalizer


class CrowdstrikeClient(SimpleBaseClient):
    API_URL = "https://api.recruiting.app.silk.security/api/crowdstrike/hosts/get"

    def __init__(self, api_key: str, limit: int = 1, skip: int = 0):
        self.api_key = api_key
        self.limit = limit
        self.skip = skip

    def get_normalizer(self):
        return CrowdstrikeNormalizer()

    def get_asset_merger(self):
        return CrowdstrikeAssetMerger()
