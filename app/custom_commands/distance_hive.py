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
        """Executes the command."""
        root = self.navigator.get_copy_root()

        last_thought = [
            key
            for key, value in root["galactic_object"].items()
            if isinstance(value, dict)
            and value.get("initializer") == '"fallen_hive_last_thought"'
        ]

        if last_thought:
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

            while open_list:
                path = open_list.popleft()

                if path[-1] == last_thought[0]:
                    found_path = path
                    break

                if path[-1] in closed_list:
                    continue
                closed_list.add(path[-1])

                for neighbor in graph.get(path[-1], []):
                    if neighbor not in closed_list:
                        open_list.append(path + [neighbor])

            if found_path:
                _logger.info(len(found_path))
            else:
                _logger.info("Distance non trouvée")
        else:
            _logger.info("Pas de fragments séparés")

        return 0
