from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Account(BaseModel):
    usernames: Optional[list]


class Bios(BaseModel):
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    version: Optional[str] = None


class UnifiedHost(BaseModel):
    # main fields
    instance_id: Optional[str]
    hostname: str
    local_ip: str
    public_ip: str
    os: str
    platform: str
    manufacturer: str
    model: str
    availability_zone: Optional[str]
    # kernel_version: str

    # with sources
    created_at: Optional[dict[str, Optional[datetime]]]
    last_seen: Optional[dict[str, Optional[datetime]]]
    service_provider: Optional[dict[str, Optional[str]]]

    # differ
    account: Optional[Account] = None

    # common
    bios: Optional[Bios] = None
    account_id: Optional[str] = None  # TODO: not sure if needed
