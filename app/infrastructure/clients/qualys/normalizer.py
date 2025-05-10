from app.domain.models import Account, Bios, UnifiedHost
from app.infrastructure.clients.base import BaseNormalizer


class QualysNormalizer(BaseNormalizer):
    def normalize(self, raw: dict) -> UnifiedHost:
        source_info = (
            raw.get("sourceInfo", {})
            .get("list", [{}])[0]
            .get("Ec2AssetSourceSimple", {})
        )
        accounts = raw.get("account", {}).get("list", [])
        agent_info = raw.get("agentInfo", {})

        usernames = [
            acc["HostAssetAccount"]["username"]
            for acc in accounts if "HostAssetAccount" in acc
        ]

        return UnifiedHost(
            instance_id=source_info.get("instanceId"),
            hostname=raw.get("dnsHostName"),
            local_ip=raw.get("address"),
            public_ip=source_info.get("publicIpAddress"),
            os=raw.get("os"),
            platform=agent_info.get("platform"),
            manufacturer=raw.get("manufacturer"),
            model=raw.get("model"),
            availability_zone=source_info.get("availabilityZone"),
            created_at={"qualys": raw.get("created")},
            last_seen={"qualys": agent_info.get("lastCheckedIn", {}).get("$date")},
            service_provider={"qualys": raw.get("cloudProvider")},
            bios=Bios(description=raw.get("biosDescription")),
            account_id=source_info.get("accountId"),

            account=Account(usernames=usernames),
        )
