import json
import logging
import os
from glob import glob

from visualisation.graph import Node, Edge


class LogDataTransformer:

    def create_graph(self):
        edges = []
        nodes = []
        for entry in self.__list_entries():
            try:
                if entry.has_data_lineage():
                    nodes.extend(entry.get_nodes())
            except KeyError:
                logging.warn("Wrong entry: {}".format(entry))
                raise
        return list(set(nodes)), edges

    def gen(self):
        upload1 = Node("cloud-upload", "id:1", "Title1",
                       properties={'prop1': 'value1'})
        upload2 = Node("cloud-upload", "id:2",
                       "Title2")
        upload3 = Node("cloud-upload", "id:2",
                       "Title3")
        cloud = Node("cloud", "id:5",
                     "Title2")
        edges = []
        edges.append(Edge(upload1, cloud, role='Upload1'))
        edges.append(Edge(upload2, cloud, role='Upload2'))
        nodes = [upload1, upload2, upload3, cloud]
        return nodes, edges

    def __list_entries(self):
        json_files = [y for x in os.walk("logs") for y in glob(os.path.join(x[0], '*.json'))]
        for json_file in json_files:
            logging.info("Parsing log entries from {}".format(json_file))
            with open(json_file) as data_file:
                json_dict = json.load(data_file)
                for entry in json_dict['entries']:
                    yield LogEntry(entry)


class LogEntry(object):

    def __init__(self, json_dict):
        self.json_dict = json_dict

    def has_data_lineage(self):
        try:
            stats = self.json_dict['protoPayload']['serviceData']['jobCompletedEvent']['job']['jobStatistics']
        except KeyError:
            return False
        return True

    def get_nodes(self):
        try:
            destination_table = \
                self.json_dict['protoPayload']['serviceData']['jobCompletedEvent']['job']['jobConfiguration']['query'][
                    'destinationTable']

            if destination_table['datasetId'].startswith("_") and destination_table['tableId'].startswith("anon"):
                return []

            return [Node("cloud-upload", self.__create_table_id(destination_table),
                         self.__create_table_id(destination_table))]
        except KeyError:
            return []

    def __create_table_id(self, table):
        return "{}.{}.{}".format(table['projectId'], table['datasetId'], table['tableId'].split('$')[0])

    def __str__(self):
        return json.dumps(self.json_dict, indent=4, sort_keys=True)
