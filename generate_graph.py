import logging
import sys

from logs_reader import LogDataReader

logging.basicConfig(
    format='%(asctime)s %(levelname)-5s %(filename)-12s %(message)s',
    level=logging.DEBUG, stream=sys.stdout)

try:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("project_ids", help="List of project ids separated by comma")
    parser.add_argument("--number_of_days", help="Limits audit logs data to last number of days", default=7, type=int)
    args = parser.parse_args()
except ImportError:
    args = None


if __name__ == '__main__':
    for project_id in args.project_ids.split(","):
        LogDataReader().download_log_entries(project_id, args.number_of_days)
