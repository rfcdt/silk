from clients.base import BaseNormalizer
from models.host import Account, AgentInfo, UnifiedHost


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
            gateway_address=raw.get('default_gateway_ip'),
            # kernel_version=raw.get('kernel_version'),
            
            created_at={'crowdstrike': raw.get('first_seen')},
            last_seen={'crowdstrike': raw.get('last_seen')},
            service_provider={'crowdstrike', raw.get('service_provider')},

            # agent_version=raw.get('agent_version'),
            # agent_info=AgentInfo(
            #     local_time=raw.get('agent_local_time')
            # ),
            # account=None,
            # is_docker_host=None,
            # last_compliance_scan=None,
            # last_logged_on_user=None,
            # last_system_boot=None,
            # last_vuln_scan=None,
            # modified=
            
        )
