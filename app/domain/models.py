from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Bios(BaseModel):
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    version: Optional[str] = None

    
class UnifiedHost(BaseModel):
    # _id: Optional[]

    # main fields
    instance_id: str
    hostname: str
    local_ip: str
    public_ip: str
    os: str
    platform: str
    manufacturer: str
    model: str
    availability_zone: str
    # kernel_version: str
    
    # with sources
    created_at: Optional[Dict[str, Optional[datetime]]]
    last_seen: Optional[Dict[str, Optional[datetime]]]
    service_provider: Optional[Dict[str, Optional[str]]] # cloudProvider & service_provider

    # gateway_address: str
    # differ
    # agent_version: Optional[str]
    # agent_info: Optional[AgentInfo]
    # account: Optional[Account]
    # is_docker_host: Optional[bool]
    # last_compliance_scan: Optional[datetime]
    # last_logged_on_user: Optional[str]
    # last_system_boot: Optional[datetime]
    # last_vuln_scan: Optional[LastVulnScan]
    # modified: Optional[datetime]
    # network_guid: Optional[str]
    # network_interface: Optional[NetworkInterface]
    # open_port: Optional[OpenPort]
    # processor: Optional[Processor]
    # qweb_host_id: Optional[int]
    # source_info: Optional[SourceInfo]
    # tags: Optional[Tags]
    # timezone: Optional[str]
    # total_memory: Optional[int]
    # tracking_method: Optional[str]
    # type: Optional[str]

    # volume: Optional[Volume]
    # vuln: Optional[Vuln]

    # cpu_signature: Optional[str]
    # policies: Optional[List[Policy]]
    # reduced_functionality_mode: Optional[str]
    # device_policies: DevicePolicies
    # status: Optional[str]

    # common
    bios: Optional[Bios] = None
    account_id: Optional[str] = None  # TODO: not sure if needed


