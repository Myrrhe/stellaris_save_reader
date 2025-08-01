# -*- coding: utf-8 -*-
"""Dummy command."""

from collections import deque
import logging
from command import Command

_logger: logging.Logger = logging.getLogger(__name__)


class DistanceHiveCommand(Command):
    """Dummy command."""

    name = "distance_hive"

    def handle(self, **options) -> int:
        root = self.navigator.get_copy_root()

        id_hive = [
            key
            for key, value in root["country"].items()
            if isinstance(value, dict)
            and value.get("personality") == '"fallen_empire_machine"'
        ]

        if id_hive:
            systems_hive = [
                key
                for key, value in root["galactic_object"].items()
                if id_hive[0] in value["starbases"]
            ]
            id_player = root["player"][0]["country"]
            systems_player = [
                key
                for key, value in root["galactic_object"].items()
                if id_player in value["starbases"]
            ]

            graph = {}
            for node_id, data in root["galactic_object"].items():
                graph.setdefault(node_id, set())
                for hl in data.get("hyperlane", []):
                    graph[node_id].add(hl["to"])
                    graph.setdefault(hl["to"], set()).add(node_id)

            open_list = deque([[systems_player[0]]])
            closed_list = set()
            found_path = []
            found = False

            while open_list:
                path = open_list.popleft()
                node = path[-1]

                if node == systems_hive[0]:
                    found = True
                    found_path = path
                    break

                if node in closed_list:
                    continue
                closed_list.add(node)

                for voisin in graph.get(node, []):
                    if voisin not in closed_list:
                        open_list.append(path + [voisin])

            if found:
                _logger.info(len(found_path))
            else:
                _logger.info("Distance non trouvée")
        else:
            _logger.info("Pas de fragments séparés")

        return 0
