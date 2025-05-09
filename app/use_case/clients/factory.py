from typing import TypeAlias

from clients.base import BaseClient

from .crowdstrike import CrowdstrikeClient
from .qualys import QualysClient


class ClientFactory:
    @staticmethod
    def get_client(key: str, api_key) -> BaseClient:
        clients = {
            'crowdstrike': (CrowdstrikeClient, api_key),
            'qualys': (QualysClient, api_key),
        }

        client = clients.get(key)
        if client is None:
            # TODO: raise custom exception
            raise Exception(f"The client {client} is not implemented")

        return client[0](client[1])
        