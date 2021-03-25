import requests
from requests.auth import HTTPDigestAuth
from requests.exceptions import HTTPError
import click
import time


class Api:
    def __init__(self, api_public, api_private, project, cluster_name):
        self.api_public = api_public
        self.api_private = api_private
        self.project = project
        self.cluster_name = cluster_name

    # https://docs.atlas.mongodb.com/reference/api/clusters-get-one/
    def get_cluster_info(self):
        response = requests.get(
            f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{self.project}/clusters/{self.cluster_name}",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=HTTPDigestAuth(self.api_public, self.api_private)
            )
        response.raise_for_status()

        return response.json()

    # https://docs.atlas.mongodb.com/reference/api/processes-get-all/
    def get_processes(self):
        response = requests.get(
            f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{self.project}/processes",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=HTTPDigestAuth(self.api_public, self.api_private)
            )
        response.raise_for_status()

        return response.json()

    # https://docs.atlas.mongodb.com/reference/api/processes-get-one/
    def get_process_by_id(self, process_id):
        response = requests.get(
            f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{self.project}/processes/{process_id}",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=HTTPDigestAuth(self.api_public, self.api_private)
            )
        response.raise_for_status()

        return response.json()

    # https://docs.atlas.mongodb.com/reference/api/logs/
    def get_process_log(self, hostname, log_name, start_date, end_date):
        response = requests.get(
            f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{self.project}/clusters/{hostname}/logs/{log_name}?"
            f"startDate={start_date}&endDate={end_date}",
            headers={"Accept": "application/gzip", "Content-Type": "application/json"},
            auth=HTTPDigestAuth(self.api_public, self.api_private)
            )
        response.raise_for_status()

        return response

    # https://docs.atlas.mongodb.com/reference/api/process-measurements/
    def get_process_measurements(self, process_id, start_date, end_date, granularity):
        response = requests.get(
            f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{self.project}/processes/{process_id}/measurements?"
            f"start={start_date}&end={end_date}&granularity={granularity}",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=HTTPDigestAuth(self.api_public, self.api_private)
            )
        response.raise_for_status()

        return response.json()
