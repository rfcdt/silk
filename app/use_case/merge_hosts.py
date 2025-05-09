

from enum import Enum
from typing import Any

from pydantic import BaseModel
from pymongo.collection import Collection

from app.domain.domain import DomainService
from app.infrastructure.mongo_repository import MongoRepository
from app.use_case.clients.factory import ClientFactory


class TestChoice(str, Enum):
    qualys = "qualys"
    crowdstrike = "crowdstrike"


class MergeHostDto(BaseModel):
    source: TestChoice
    collection: Collection
    api_key: str


class MergeHostUseCase:
    def merge(self, dto: MergeHostDto):
        repository = MongoRepository(collection=dto.collection)

        client = ClientFactory.get_client(dto.source, dto.api_key)

        domain_service = DomainService(client, repository)
        domain_service.merge_hosts()
