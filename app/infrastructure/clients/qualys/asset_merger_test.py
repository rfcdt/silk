from datetime import datetime

from app.domain.models import Bios, UnifiedHost

from .asset_merger import QualysAssetMerger


class TestAssetMerger:
    def setup_method(self, test_method):
        self.asset_merger = QualysAssetMerger()
        self.source_data = UnifiedHost(
            instance_id="qwerty",
            hostname="localhost",
            local_ip="127.0.0.1",
            public_ip="172.17.0.2",
            os="Amazon Linux 2",
            platform="Linuex",
            manufacturer="Xen",
            model="HVM domU",
            availability_zone="us-east-1c",
            created_at={"qualys": datetime(2024, 1, 1)},
            last_seen={"qualys": datetime(2024, 5, 1)},
            service_provider={"qualys": "AWS"},
            bios=Bios(description="Xen BIOS"),
        )

    def test_merge_when_existing_has_no_bios(self):
        existing = UnifiedHost(
            instance_id="qwerty",
            hostname="localhost",
            local_ip="127.0.0.1",
            public_ip="172.17.0.2",
            os="Amazon Linux 2",
            platform="Linuex",
            manufacturer="Xen",
            model="HVM domU",
            availability_zone="us-east-1c",
            created_at={},
            last_seen={},
            service_provider={},
            bios=None,
        )

        self.asset_merger.merge(self.source_data, existing)

        assert existing.created_at["qualys"] == datetime(2024, 1, 1)
        assert existing.last_seen["qualys"] == datetime(2024, 5, 1)
        assert existing.service_provider["qualys"] == "AWS"
        assert existing.bios.description == "Xen BIOS"

    def test_merge_when_existing_has_bios(self):
        existing = UnifiedHost(
            instance_id="qwerty",
            hostname="localhost",
            local_ip="127.0.0.1",
            public_ip="172.17.0.2",
            os="Amazon Linux 2",
            platform="Linuex",
            manufacturer="Xen",
            model="HVM domU",
            availability_zone="us-east-1c",
            created_at={},
            last_seen={},
            service_provider={},
            bios=Bios(description="Old BIOS"),
        )

        self.asset_merger.merge(self.source_data, existing)

        assert existing.bios.description == "Xen BIOS"
