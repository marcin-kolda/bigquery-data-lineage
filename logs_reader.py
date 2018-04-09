import json
import logging
import os
import datetime
from googleapiclient.discovery import build

from oauth2client.client import GoogleCredentials


class LogDataReader:

    def __init__(self):
        credentials = GoogleCredentials.get_application_default()
        self.logging_service = build('logging', 'v2', credentials=credentials)

    def download_log_entries(self, project_id, number_of_days):
        logging.info("Downloading bigquery logs from last {} days from project {}".format(number_of_days, project_id))
        for entry_list in self.__iterate_over_log_entries(project_id, number_of_days):
            filename = "logs/" + project_id + "/" + project_id + "_" + \
                       (entry_list['nextPageToken'] if 'nextPageToken' in entry_list else "") + ".json"
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            with open(filename, 'w') as data_file:
                json.dump(entry_list, data_file)

    def __iterate_over_log_entries(self, project_id, number_of_days):
        timestamp = (datetime.datetime.utcnow() + datetime.timedelta(days=-number_of_days)).isoformat("T") + "Z"
        body = {
            "resourceNames": [
                "projects/" + project_id
            ],
            "pageSize": 300,
            "filter": "resource.type = \"bigquery_resource\" AND timestamp >= \"" + timestamp + "\""
        }
        response = self.logging_service.entries().list(body=body).execute(num_retries=7)

        while response:
            yield response

            if 'nextPageToken' in response:
                body['pageToken'] = response['nextPageToken']
                response = self.logging_service.entries().list(body=body).execute(num_retries=7)
            else:
                response = None
