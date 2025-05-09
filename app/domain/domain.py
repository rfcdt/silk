from typing import Any, Dict, Iterator, List, Optional, Protocol

from .models import UnifiedHost


class IRepository(Protocol):
    def find_all(self) -> List[Dict[str, Any]]:
        pass

    def find_by_filter(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    def save_one(self, document: Dict[str, Any]) -> Any:
        pass

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> Any:
        pass

    def save_many(self, query: Dict[str, Any], update: Dict[str, Any]) -> Any:
        pass


class IClient(Protocol):
    def fetch_hosts(self) -> Iterator[UnifiedHost]:
        pass


class DomainService:
    COMPOUND_KEY_STR = (
        "{instance_id}_"
        "{hostname}_"
        "{local_ip}_"
        "{public_ip}_"
        "{os}_"
        "{platform}_"
        "{manufacturer}_"
        "{model}_"
        "{availability_zone}_"
        "{gateway_address}"
    )

    def __init__(self, client: IClient, repository: IRepository):
        self.client = client
        self.repository = repository

    def merge_hosts(self):
        # maybe use pandas or pyspark to determine duplicates

        iterator_hosts = self.client.fetch_hosts()
        print("=================")

        print(iterator_hosts)

        hosts = [item for item in iterator_hosts]

        compound_hosts_for_filtering = self.get_generate_hosts_for_filtering(hosts)
        possible_duplicates_dict = self.get_possible_duplicates(
            compound_hosts_for_filtering
        )



        result_to_save = []

        i = 0
        for host in hosts:
            i += 1

            duplicate = possible_duplicates_dict.get(
                self.COMPOUND_KEY_STR.format(
                    host.instance_id,
                    host.hostname,
                    host.local_ip,
                    host.public_ip,
                    host.os,
                    host.platform,
                    host.manufacturer,
                    host.model,
                    host.availability_zone,
                    host.gateway_address,
                )
            )

            if duplicate:
                ...
            else:
                result_to_save.append(host)

        self.repository.save_many(result_to_save)


    def get_generate_hosts_for_filtering(self, hosts: List[UnifiedHost]):
        return [
            {
                "instance_id": host.instance_id,
                "hostname": host.hostname,
                "local_ip": host.local_ip,
                "public_ip": host.public_ip,
                "os": host.os,
                "platform": host.platform,
                "manufacturer": host.manufacturer,
                "model": host.model,
                "availability_zone": host.availability_zone,
                "gateway_address": host.gateway_address,
            }
            for host in hosts
        ]

    def get_possible_duplicates(self, compound_hosts_for_filtering) -> Dict[str, Any]:
        possible_duplicates_query = self.repository.find_by_filter(
            {"$or": compound_hosts_for_filtering}
        )

        # generate a dict with a key as a string to get it inside the loop
        return {
            self.COMPOUND_KEY_STR.format(
                possible_duplicate.instance_id,
                possible_duplicate.hostname,
                possible_duplicate.local_ip,
                possible_duplicate.public_ip,
                possible_duplicate.os,
                possible_duplicate.platform,
                possible_duplicate.manufacturer,
                possible_duplicate.model,
                possible_duplicate.availability_zone,
                possible_duplicate.gateway_address,
            ): possible_duplicate
            for possible_duplicate in possible_duplicates_query
        }
