import logging
import sys

from logs_reader import LogDataReader
from logs_transformer import LogDataTransformer
from visualisation import template_renderer

logging.basicConfig(
    format='%(asctime)s %(levelname)-5s %(filename)-12s %(message)s',
    level=logging.DEBUG, stream=sys.stdout)

try:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("project_ids", help="List of project ids separated by comma")
    parser.add_argument("--number_of_days", help="Limits audit logs data to last number of days", default=7, type=int)
    parser.add_argument("--ignore", help="List ignored project ids separated by comma")
    args = parser.parse_args()
except ImportError:
    args = None


if __name__ == '__main__':
    for project_id in args.project_ids.split(","):
        LogDataReader().download_log_entries(project_id, args.number_of_days)
    ignored_projects_ids = args.ignore.split(',')
    logging.info("Ignored project ids: {}".format(ignored_projects_ids))
    nodes, edges = LogDataTransformer(ignored_projects_ids).create_graph()
    with open('nodes.json', 'w') as data_file:
        data_file.write("\n".join([n.__str__() for n in nodes]))
    with open('edges.json', 'w') as data_file:
        data_file.write("\n".join([n.__str__() for n in edges]))
    template_renderer.render(nodes, edges, 'graph.html')
