from app.domain.models import Bios, UnifiedHost
from app.infrastructure.clients.base import BaseNormalizer


class CrowdstrikeNormalizer(BaseNormalizer):
    
    def normalize(self, raw: dict):
        return UnifiedHost(
            instance_id=raw.get('instance_id'),
            hostname=raw.get("hostname"),
            local_ip=raw.get('local_ip'),
            public_ip=raw.get('external_ip'),
            os=raw.get('os_version'),
            platform=raw.get('platform_name'),
            manufacturer=raw.get('system_manufacturer'),
            model=raw.get('system_product_name'),
            availability_zone=raw.get('zone_group'),
            # gateway_address=raw.get('default_gateway_ip'),
            
            created_at={'crowdstrike': raw.get('first_seen')},
            last_seen={'crowdstrike': raw.get('last_seen')},
            service_provider={'crowdstrike': raw.get('service_provider')},

            bios=Bios(
                manufacturer=raw.get('bios_manufacturer'),
                version=raw.get('bios_version')
            ),
            account_id=raw.get('service_provider_account_id'),
        )
