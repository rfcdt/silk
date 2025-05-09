from typing import Any, Dict, Iterator, List, Optional, Protocol

from .models import UnifiedHost


class IRepository(Protocol):
    def find_by_filter(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    def save_many(self, data: List[Dict[str, Any]]) -> Any:
        pass

    def update_many(self, data: List[Dict[str, Any]]) -> Any:
        pass


class IClient(Protocol):
    def fetch_hosts(self) -> Iterator[UnifiedHost]:
        pass


class IAssetMerger(Protocol):
    def merge(self, source_data: UnifiedHost, existing: UnifiedHost):
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
        "{availability_zone}"
        # "{gateway_address}"
    )

    def __init__(
        self, client: IClient, repository: IRepository, asset_merger: IAssetMerger
    ):
        self.client = client
        self.repository = repository
        self.asset_merger = asset_merger

    def merge_hosts(self):
        print("=================")
        # maybe use pandas or pyspark to determine duplicates

        # TODO: it retrive only one limit+skip. fix
        iterator_hosts = self.client.fetch_hosts()

        hosts = [item for item in iterator_hosts]
        # print(hosts)

        compound_hosts_for_filtering = self.get_generate_hosts_for_filtering(hosts)
        # retrive possible duplicated hosts
        # it doesn't retrive the whole collection as we have filters
        # and in the current itera
        possible_duplicates_dict = self.get_possible_duplicates(
            compound_hosts_for_filtering
        )

        result_to_save = []
        result_to_update = []

        for host in hosts:
            duplicate = possible_duplicates_dict.get(
                self.COMPOUND_KEY_STR.format(
                    instance_id=host.instance_id,
                    hostname=host.hostname,
                    local_ip=host.local_ip,
                    public_ip=host.public_ip,
                    os=host.os,
                    platform=host.platform,
                    manufacturer=host.manufacturer,
                    model=host.model,
                    availability_zone=host.availability_zone,
                    # gateway_address=host.gateway_address,
                )
            )

            if duplicate:
                self.asset_merger.merge(host, duplicate)

                duplicate_dict = duplicate.model_dump()
                result_to_update.append(duplicate_dict)
            else:
                result_to_save.append(host.model_dump())

        self.repository.save_many(result_to_save)
        self.repository.update_many(result_to_update)

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
                # "gateway_address": host.gateway_address,
            }
            for host in hosts
        ]

    def get_possible_duplicates(self, compound_hosts_for_filtering) -> Dict[str, Any]:
        possible_duplicates_query = self.repository.find_by_filter(
            {"$or": compound_hosts_for_filtering}  # TODO: move "or" out of here
        )
        # generate a dict with a key as a string to get it inside the loop
        return {
            self.COMPOUND_KEY_STR.format(
                instance_id=possible_duplicate["instance_id"],
                hostname=possible_duplicate["hostname"],
                local_ip=possible_duplicate["local_ip"],
                public_ip=possible_duplicate["public_ip"],
                os=possible_duplicate["os"],
                platform=possible_duplicate["platform"],
                manufacturer=possible_duplicate["manufacturer"],
                model=possible_duplicate["model"],
                availability_zone=possible_duplicate["availability_zone"],
                # gateway_address=possible_duplicate.gateway_address,
            ): UnifiedHost(**possible_duplicate)
            for possible_duplicate in possible_duplicates_query
        }
