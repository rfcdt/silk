from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, model_validator

# ---- agen info

class ManifestVersion(BaseModel):
    sca: str
    vm: str


class ActivationKey(BaseModel):
    title: str
    activation_id: str


class AgentConfiguration(BaseModel):
    id: int
    name: str


class LastCheckedIn(BaseModel):
    date: datetime = Field(..., alias="$date")
    

class AgentInfo(BaseModel):
    location: str
    location_geo_latitude: str
    last_checked_in: LastCheckedIn
    location_geo_longtitude: str
    agent_version: str
    manifest_version: ManifestVersion
    activated_module: str
    activation_key: ActivationKey
    agent_configuration: AgentConfiguration
    status: str
    chirp_status: str
    connected_from: str
    agent_id: str

    local_time: datetime



class Bios(BaseModel):
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    version: Optional[str] = None


class SourceInfo(BaseModel):
    private_ip: Optional[str] = None
    vpc_id: Optional[str] = None
    subnet_id: Optional[str] = None



class Account(BaseModel):
    list: list[dict[dict[dict]]]



class LastVulnScan(BaseModel):
    date: datetime = Field(..., alias="$date")
    

## networkInterface
class HostAssetInterface(BaseModel):
    interfaceName: Optional[str]
    macAddress: Optional[str]
    gatewayAddress: Optional[str]
    address: str
    hostname: str


class NetworkInterfaceItem(BaseModel):
    HostAssetInterface: HostAssetInterface


class NetworkInterface(BaseModel):
    list: List[NetworkInterfaceItem]
## networkInterface



## open port
class HostAssetOpenPort(BaseModel):
    serviceName: str
    protocol: str
    port: int


class OpenPortItem(BaseModel):
    HostAssetOpenPort: HostAssetOpenPort


class OpenPort(BaseModel):
    list: List[OpenPortItem]
## open port

## processor
class HostAssetProcessor(BaseModel):
    name: str
    speed: Optional[int] = None  # in MHz

class ProceesorItem(BaseModel):
    HostAssetProcessor: HostAssetProcessor

class Processor(BaseModel):
    list: List[ProceesorItem]
## processor


## software
class HostAssetSoftware(BaseModel):
    name: str
    version: str

class SoftwareItem(BaseModel):
    HostAssetSoftware: HostAssetSoftware

class Software(BaseModel):
    list: List[SoftwareItem]
## software


## source info

class Ec2InstanceTags(BaseModel):
    tags: Dict[str, List]  # The list is empty here, but this allows flexibility


class Ec2AssetSourceSimple(BaseModel):
    instanceType: str
    subnetId: str
    imageId: str
    groupName: str
    accountId: str
    macAddress: str
    reservationId: str
    instanceId: str
    monitoringEnabled: str
    spotInstance: str
    zone: str
    instanceState: str
    privateDnsName: str
    vpcId: str
    type: str
    availabilityZone: str
    privateIpAddress: str
    firstDiscovered: datetime
    ec2InstanceTags: Ec2InstanceTags
    publicIpAddress: str
    lastUpdated: datetime
    region: str
    assetId: int
    groupId: str
    localHostname: str
    publicDnsName: str


class AssetSource(BaseModel):
    # Accepts any valid structure, currently empty
    pass


class SourceInfoItem(BaseModel):
    ec2AssetSourceSimple: Optional[Ec2AssetSourceSimple] = None
    assetSource: Optional[AssetSource] = None


class SourceInfo(BaseModel):
    list: List[SourceInfoItem]

## source info


## tag

class TagSimple(BaseModel):
    id: int
    name: str


class TagItem(BaseModel):
    TagSimple: TagSimple


class Tags(BaseModel):
    list: List[TagItem]

## tag


## volume

class LongIntWrapper(BaseModel):
    # Handles values like {"$numberLong": "123456"}
    __root__: Union[int, dict]

    @model_validator(pre=True)
    def extract_long(cls, values):
        if isinstance(values, dict) and "$numberLong" in values:
            return int(values["$numberLong"])
        return values


class HostAssetVolume(BaseModel):
    free: Union[int, LongIntWrapper]
    name: str
    size: Union[int, LongIntWrapper]

    @model_validator(pre=True)
    def unwrap_numbers(cls, values):
        if isinstance(values.get("free"), dict):
            values["free"] = LongIntWrapper.parse_obj(values["free"]).__root__
        if isinstance(values.get("size"), dict):
            values["size"] = LongIntWrapper.parse_obj(values["size"]).__root__
        return values


class VolumeItem(BaseModel):
    HostAssetVolume: HostAssetVolume


class Volume(BaseModel):
    list: List[VolumeItem]

## volume


## vuln
class HostInstanceVulnIdWrapper(BaseModel):
    __root__: Union[int, dict]

    @model_validator(pre=True)
    def extract_id(cls, values):
        if isinstance(values, dict) and "$numberLong" in values:
            return int(values["$numberLong"])
        return values


class HostAssetVuln(BaseModel):
    hostInstanceVulnId: Union[int, HostInstanceVulnIdWrapper]
    lastFound: datetime
    firstFound: datetime
    qid: int

    @model_validator(pre=True)
    def unwrap_vuln_id(cls, values):
        if isinstance(values.get("hostInstanceVulnId"), dict):
            values["hostInstanceVulnId"] = HostInstanceVulnIdWrapper.parse_obj(values["hostInstanceVulnId"]).__root__
        return values


class VulnItem(BaseModel):
    HostAssetVuln: HostAssetVuln


class Vuln(BaseModel):
    list: List[VulnItem]
## vuln


class ModifiedTimestamp(BaseModel):
    # Handles {"$date": "2023-03-16T13:34:51.000Z"}
    __root__: Union[datetime, Dict[str, str]]

    @model_validator(pre=True)
    def extract_date(cls, values):
        if isinstance(values, dict) and "$date" in values:
            return datetime.fromisoformat(values["$date"].replace("Z", "+00:00"))
        return values


class Policy(BaseModel):
    policy_type: str
    policy_id: str
    applied: bool
    settings_hash: str
    assigned_date: Optional[datetime]
    applied_date: Optional[datetime]
    rule_groups: Optional[List] = []
    uninstall_protection: Optional[str] = None


class DevicePolicies(BaseModel):
    prevention: Optional[Policy]
    sensor_update: Optional[Policy]
    global_config: Optional[Policy]
    remote_response: Optional[Policy]


class Meta(BaseModel):
    version: str
    version_string: str


class DeviceAsset(BaseModel):
    agent_load_flags: str
    agent_local_time: datetime
    agent_version: str
    
    product_type_desc: str
    provision_status: str
    serial_number: str
    status: str
    tags: List = []
    modified_timestamp: ModifiedTimestamp
    chassis_type: str
    chassis_type_desc: str
    connection_ip: str




class UnifiedHost(BaseModel):
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
    gateway_address: str
    # kernel_version: str
    
    # with sources
    created_at: Optional[Dict[str, Optional[datetime]]]
    last_seen: Optional[Dict[str, Optional[datetime]]]
    service_provider: Optional[Dict[str, Optional[str]]] # cloudProvider & service_provider

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
    bios: Optional[Bios]
    account_id: str # TODO: not sure if needed

