import unittest

from log_entry import LogEntry


class TestLogEntry(unittest.TestCase):

    def test_normalize_table_id(self):
        table_dict = {'projectId': 'p', 'datasetId': 'd', 'tableId': 't'}
        table_id = LogEntry.normalize_table_id(table_dict)

        self.assertEqual("p.d.t", table_id)

    def test_normalize_partition(self):
        table_dict = {'projectId': 'p', 'datasetId': 'd', 'tableId': 't$partition'}
        table_id = LogEntry.normalize_table_id(table_dict)

        self.assertEqual("p.d.t", table_id)

    def test_normalize_sharded_table(self):
        table_dict = {'projectId': 'p', 'datasetId': 'd', 'tableId': 't_20180407'}
        table_id = LogEntry.normalize_table_id(table_dict)

        self.assertEqual("p.d.t_*", table_id)

    def test_normalize_table_with_double_date(self):
        table_dict = {'projectId': 'p', 'datasetId': 'd', 'tableId': 'table_v1_20180407_201804072200'}
        table_id = LogEntry.normalize_table_id(table_dict)

        self.assertEqual("p.d.table_v1_*", table_id)
