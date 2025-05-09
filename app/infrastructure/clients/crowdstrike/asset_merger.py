from app.domain.models import Bios, UnifiedHost
from app.infrastructure.clients.base import AssetMerger


class CrowdstrikeAssetMerger(AssetMerger):
    def merge(self, source_data: UnifiedHost, existing: UnifiedHost):
        existing.created_at["crowdstrike"] = source_data.created_at["crowdstrike"]
        existing.last_seen["crowdstrike"] = source_data.last_seen["crowdstrike"]
        existing.service_provider["crowdstrike"] = source_data.service_provider[
            "crowdstrike"
        ]
        if existing.bios is None:
            existing.bios = Bios(
                manufacturer=source_data.bios.manufacturer,
                version=source_data.bios.version,
            )
        else:
            existing.bios.manufacturer = source_data.bios.manufacturer
            existing.bios.version = source_data.bios.version
