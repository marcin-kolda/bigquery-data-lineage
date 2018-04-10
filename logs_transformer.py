import json
import logging
import os
from glob import glob

from log_entry import LogEntry
from visualisation.graph import Edge


class LogDataTransformer:

    def __init__(self, ignored_projects_ids):
        self.ignored_projects_ids = ignored_projects_ids

    def create_graph(self):
        edges = []
        nodes = []
        for entry in self.__list_entries():
            try:
                if entry.has_data_lineage() and entry.get_destination_project() not in self.ignored_projects_ids:
                    target_node = entry.get_target_node()
                    if not target_node:
                        continue
                    nodes.append(target_node)
                    source_nodes = entry.get_source_nodes()
                    if not source_nodes:
                        continue
                    nodes.extend(source_nodes)
                    for source_node in source_nodes:
                        edges.append(Edge(source_node, target_node, role='Upload1'))
            except KeyError:
                logging.warn("Wrong entry: {}".format(entry))
                raise
        return list(set(nodes)), list(set(edges))

    @staticmethod
    def __list_entries():
        json_files = [y for x in os.walk("logs") for y in glob(os.path.join(x[0], '*.json'))]
        for json_file in json_files:
            logging.info("Parsing log entries from {}".format(json_file))
            with open(json_file) as data_file:
                json_dict = json.load(data_file)
                for entry in json_dict['entries']:
                    yield LogEntry(entry)
