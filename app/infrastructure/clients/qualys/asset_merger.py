from app.domain.models import UnifiedHost
from app.infrastructure.clients.base import AssetMerger


class QualysAssetMerger(AssetMerger):
    def merge(self, source_data: dict, existing: UnifiedHost):
        existing.created_at["qualys"] = existing.get("first_seen")
        existing.last_seen["qualys"] = existing.get("last_seen")
        existing.service_provider["qualys"] = existing.get("service_provider")
