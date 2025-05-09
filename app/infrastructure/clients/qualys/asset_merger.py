from app.domain.models import Bios, UnifiedHost
from app.infrastructure.clients.base import AssetMerger


class QualysAssetMerger(AssetMerger):
    def merge(self, source_data: UnifiedHost, existing: UnifiedHost):
        existing.created_at["qualys"] = source_data.created_at["qualys"]
        existing.last_seen["qualys"] = source_data.last_seen["qualys"]
        existing.service_provider["qualys"] = source_data.service_provider["qualys"]

        if existing.bios is None:
            existing.bios = Bios(description=source_data.bios.description)
        else:
            existing.bios.description = source_data.bios.description
