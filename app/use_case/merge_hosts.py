from dataclasses import dataclass
from enum import Enum

from pymongo.collection import Collection

from app.domain.domain import DomainService
from app.infrastructure.clients import ClientFactory
from app.infrastructure.mongo_repository import MongoRepository


class TestChoice(str, Enum):
    qualys = "qualys"
    crowdstrike = "crowdstrike"


@dataclass
class MergeHostDto:
    source: TestChoice
    collection: Collection
    api_key: str


class MergeHostUseCase:
    def merge(self, dto: MergeHostDto):
        repository = MongoRepository(collection=dto.collection)

        client = ClientFactory.get_client(dto.source, dto.api_key)

        domain_service = DomainService(client, repository, client.get_asset_merger())
        domain_service.merge_hosts()
