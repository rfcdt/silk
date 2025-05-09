from app.domain.models import UnifiedHost
from app.use_case.clients.base import BaseNormalizer


class QualysNormalizer(BaseNormalizer):
    
    def normalize(self, raw: dict):
        source_info = raw.get("sourceInfo", {}).get("list", [{}])[0].get("Ec2AssetSourceSimple", {})
        host_asset_interface = raw.get("networkInterface", {}).get("list", [{}])[0].get('HostAssetInterface', {})
        accounts = raw.get("account", {}).get("list", [])
        open_ports = raw.get("openPort", {}).get("list", [])
        processors = raw.get("processor", {}).get("list", [])
        agent_info = raw.get("agentInfo", {})



        return UnifiedHost(
            instance_id=source_info.get('instanceId'),
            hostname=raw.get("dnsHostName"),
            local_ip=raw.get('address'),
            public_ip=source_info.get('publicIpAddress'),
            os=raw.get('os'),
            platform=agent_info.get('platform'),
            manufacturer=raw.get('manufacturer'),
            model=raw.get('model'),
            availability_zone=source_info.get('availabilityZone'),
            gateway_address=host_asset_interface.get('gatewayAddress'),

            created_at={'qualys': raw.get('first_seen')},
            last_seen={'qualys': raw.get('last_seen')},
            service_provider={'qualys', raw.get('service_provider')},

            # hostname=raw.get("fqdn"),
            # os=raw.get("os"),
            # kernel_version=None,
            # manufacturer=raw.get("manufacturer"),
            # model=raw.get("model"),
            # cloud=CloudInfo(
            #     provider=raw.get("cloudProvider"),
            #     region=cloud_info.get("region"),
            #     availability_zone=cloud_info.get("availabilityZone"),
            #     instance_type=cloud_info.get("instanceType"),
            #     instance_id=cloud_info.get("instanceId"),
            #     public_ip=cloud_info.get("publicIpAddress"),
            #     private_ip=cloud_info.get("privateIpAddress"),
            #     vpc_id=cloud_info.get("vpcId"),
            #     subnet_id=cloud_info.get("subnetId"),
            # ),
            # agent=AgentInfo(
            #     version=agent_info.get("agentVersion"),
            #     platform=agent_info.get("platform"),
            #     last_checkin=agent_info.get("lastCheckedIn", {}).get("$date"),
            #     status=agent_info.get("status")
            # ),
            # network_interfaces=[
            #     NetworkInterface(
            #         address=iface["HostAssetInterface"]["address"],
            #         mac_address=iface["HostAssetInterface"].get("macAddress"),
            #         hostname=iface["HostAssetInterface"].get("hostname"),
            #         gateway_address=iface["HostAssetInterface"].get("gatewayAddress")
            #     )
            #     for iface in interfaces if "HostAssetInterface" in iface
            # ],
            # open_ports=[
            #     OpenPort(
            #         port=port["HostAssetOpenPort"]["port"],
            #         protocol=port["HostAssetOpenPort"]["protocol"],
            #         service_name=port["HostAssetOpenPort"].get("serviceName")
            #     )
            #     for port in open_ports if "HostAssetOpenPort" in port
            # ],
            # accounts=[
            #     HostAccount(username=acc["HostAssetAccount"]["username"])
            #     for acc in accounts if "HostAssetAccount" in acc
            # ],
            # processors=[
            #     Processor(
            #         name=cpu["HostAssetProcessor"]["name"],
            #         speed=cpu["HostAssetProcessor"].get("speed")
            #     )
            #     for cpu in processors if "HostAssetProcessor" in cpu
            # ],
            # last_seen=raw.get("modified"),
            # created_at=raw.get("created")
        )
