import json
import re

from visualisation.graph import Node


class LogEntry(object):

    def __init__(self, json_dict):
        self.json_dict = json_dict

    def has_data_lineage(self):
        try:
            self._get_job_statistics()
        except KeyError:
            return False
        return True

    def _get_job_statistics(self):
        return self.json_dict['protoPayload']['serviceData']['jobCompletedEvent']['job']['jobStatistics']

    def get_target_node(self):
        table = self.get_destination_table()
        if table:
            return self._create_node(table)
        else:
            return None

    def _create_node(self, table):
        return Node("cloud-upload", self.normalize_table_id(table), self.normalize_table_id(table))

    def get_source_nodes(self):
        job_statistics = self._get_job_statistics()
        nodes = []
        if 'referencedViews' in job_statistics:
            nodes.extend([self._create_node(v) for v in job_statistics['referencedViews']])
        if 'referencedTables' in job_statistics:
            nodes.extend([self._create_node(v) for v in job_statistics['referencedTables']])

        return nodes

    def get_destination_table(self):
        try:
            destination_table = \
                self.json_dict['protoPayload']['serviceData']['jobCompletedEvent']['job']['jobConfiguration']['query'][
                    'destinationTable']

            if destination_table['datasetId'].startswith("_") and destination_table['tableId'].startswith("anon"):
                return None

            return destination_table
        except KeyError:
            return None

    @staticmethod
    def normalize_table_id(table_dict):
        table_name = table_dict['tableId'].split('$')[0]
        table_name = re.sub(r'(.*)_([0-9]{8}_[0-9]{12})', r'\1_*', table_name)
        table_name = re.sub(r'(.*)_([0-9]{8})', r'\1_*', table_name)
        return "{}.{}.{}".format(table_dict['projectId'], table_dict['datasetId'], table_name)

    def __str__(self):
        return json.dumps(self.json_dict, indent=4, sort_keys=True)

    def get_destination_project(self):
        table = self.get_destination_table()
        return table['projectId'] if table else None
