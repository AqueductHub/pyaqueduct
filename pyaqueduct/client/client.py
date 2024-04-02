"""Aqueduct client class to enable experiment based operations."""

import logging
import os
from datetime import date
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from gql import Client
from gql.client import SyncClientSession
from gql.transport.httpx import HTTPXTransport
from httpx import WriteTimeout, post, stream
from pydantic import BaseModel, HttpUrl, PrivateAttr
from tqdm import tqdm

from pyaqueduct.client.types import ExperimentData, ExperimentsInfo, TagsData
from pyaqueduct.exceptions import (
    InterruptedDownloadException,
    InterruptedUploadException,
)
from pyaqueduct.schemas.mutations import (
    add_tag_to_experiment_mutation,
    create_experiment_mutation,
    remove_tag_from_experiment_mutation,
    update_experiment_mutation,
)
from pyaqueduct.schemas.queries import (
    get_all_tags_query,
    get_experiment_query,
    get_experiments_query,
)


class AqueductClientResponse(BaseModel):
    """Response of methods of Aqueduct client"""

    result: str
    message: str


class AqueductClient(BaseModel):
    """
    AqueductClient - A client class for managing experiments, tags and files.

    This class provides methods for creating experiments, updating experiments,
    adding and removing tags, as well as uploading and downloading files.

    """

    url: HttpUrl
    timeout: float
    _gql_client: Client = PrivateAttr()
    _session: SyncClientSession = PrivateAttr()

    def __init__(self, url: str, timeout: float):
        """
        Args:
            url: URL of the Aqueduct server endpoint.
            timeout: Response timeout in seconds.

        """
        super().__init__(url=url, timeout=timeout)

        self._gql_client = Client(
            transport=HTTPXTransport(url=f"{url}/graphql", timeout=self.timeout)
        )
        self.connect()

    def connect(self):
        """Connect to GraphQL connect"""
        self._session = self._gql_client.connect_sync()  # type: ignore

    def close(self):
        """Close connection with GraphQL client"""
        self._gql_client.close_sync()

    def create_experiment(
        self, title: str, description: str, tags: Optional[List[str]] = None
    ) -> ExperimentData:
        """
        Create an experiment with title, description and list of tags

        Args:
        - title (str): Title of experiment
        - description (str): Description of experiment
        - tags (List[str]): List of tags to be assigned to experiment

        Returns:
        Experiment: Experiment objects having all fields
        """

        experiment = self._session.execute(
            create_experiment_mutation,
            variable_values={"title": title, "description": description, "tags": tags or []},
        )

        experiment_obj = ExperimentData.from_dict(
            experiment["createExperiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Created experiment - %s - %s", experiment_obj.id, experiment_obj.title)
        return experiment_obj

    def update_experiment(
        self, experiment_uuid: str, title: Optional[str] = None, description: Optional[str] = None
    ) -> ExperimentData:
        """
        Update title or description or both for experiment

        Args:
        - experiment_uuid (UUID): UUID of experiment to be updated
        - title (str): New title of experiment
        - description (str): New description of experiment

        Returns:
        Experiment: Experiment object with updated fields
        """
        if title and title == "":
            raise ValueError("Title cannot be an empty string")

        if description and description == "":
            raise ValueError("Description cannot be an empty string")

        experiment = self._session.execute(
            update_experiment_mutation,
            variable_values={
                "experimentId": experiment_uuid,
                "title": title,
                "description": description,
            },
        )
        experiment_obj = ExperimentData.from_dict(
            experiment["updateExperiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Updated experiment - %s", experiment_obj.id)
        return experiment_obj

    def get_experiments(
        self,
        limit: int,
        offset: int,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> ExperimentsInfo:
        """
        Get a list of experiments

        Args:
        - limit (int): Number of experiments to be fetched
        - offset (offset): Number of experiments to skip
        - title (str): Perform search on experiments through title
        - tags (List[str]): Get experiments having these tags
        - start_date (date): Start date to filter experiments
        - end_date (date): End date to filter experiments to

        Returns:
        List[Experiment]: A list of experiments with filters applied
        """
        if limit <= 0:
            raise ValueError("Limit should be a positive number")

        experiments = self._session.execute(
            get_experiments_query,
            variable_values={
                "limit": limit,
                "offset": offset,
                "title": title,
                "start_date": start_date,
                "end_date": end_date,
                "tags": tags or [],
            },
        )

        experiments_obj = ExperimentsInfo.from_dict(
            experiments["experiments"]  # pylint: disable=unsubscriptable-object
        )
        logging.info(
            "Fetched %s experiments, total %s experiments",
            len(experiments_obj.experiments),
            experiments_obj.total_count,
        )
        return experiments_obj

    def get_experiment(self, experiment_uuid: str) -> ExperimentData:
        """
        Get an Experiment by ID or Alias

        Args:
        - id_ (str): "UUID | ALIAS" Unique identifier to be used
        - value (str): Value of unique identifier to use for fetching experiment

        Returns:
        Experiment: Experiment object having all fields
        """
        experiment = self._session.execute(
            get_experiment_query, variable_values={"type": "UUID", "value": experiment_uuid}
        )

        experiment_obj = ExperimentData.from_dict(
            experiment["experiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Fetched experiment - %s", experiment_obj.title)
        return experiment_obj

    def get_experiment_by_alias(self, alias: str) -> ExperimentData:
        """
        Get an Experiment by ID or Alias

        Args:
        - id_ (str): "UUID | ALIAS" Unique identifier to be used
        - value (str): Value of unique identifier to use for fetching experiment

        Returns:
        Experiment: Experiment object having all fields
        """
        experiment = self._session.execute(
            get_experiment_query, variable_values={"type": "ALIAS", "value": alias}
        )

        experiment_obj = ExperimentData.from_dict(
            experiment["experiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Fetched experiment - %s", experiment_obj.title)
        return experiment_obj

    def add_tag_to_experiment(self, experiment_uuid: str, tag: str) -> ExperimentData:
        """
        Add a tag to an experiment

        Args:
        - experiment_uuid (UUID): UUID of experiment to which tag is to be added
        - tag (str): Tag to be added to experiment

        Returns:
        Experiment: Experiment having tag added
        """

        experiment = self._session.execute(
            add_tag_to_experiment_mutation,
            variable_values={"experimentId": experiment_uuid, "tag": tag},
        )
        experiment_obj = ExperimentData.from_dict(
            experiment["addTagToExperiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Added tag %s to experiment <%s>", tag, experiment_obj.title)
        return experiment_obj

    def remove_tag_from_experiment(self, experiment_uuid: str, tag: str) -> ExperimentData:
        """
        Remove a tag from an experiment

        Args:
        - experiment_uuid (UUID): UUID of experiment frin which tag has to be removed
        - tag (str): Tag to be removed from experiment

        Returns:
        Experiment: Experiment having tag removed
        """

        experiment = self._session.execute(
            remove_tag_from_experiment_mutation,
            variable_values={"experimentId": experiment_uuid, "tag": tag},
        )

        experiment_obj = ExperimentData.from_dict(
            experiment["removeTagFromExperiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Removed tag %s from experiment <%s>", tag, experiment_obj.title)
        return experiment_obj

    def upload_file(self, experiment_uuid: UUID, file: str) -> AqueductClientResponse:
        """
        Upload file to a specific experiment.

        Args:
            experiment_uuid : The ID of the experiment.
            file_path: The local path to the file to be uploaded.

        Returns:
            Operation results object.

        """

        headers = {
            "file_name": os.path.basename(file),
        }

        upload_url = f"{self.url}/files/{str(experiment_uuid)}"
        with open(file, "rb") as files:
            try:
                resp = post(
                    upload_url, headers=headers, timeout=self.timeout, files={"file": files}
                )
            except InterruptedUploadException as exception:
                return AqueductClientResponse(result="failed", message=exception.message)

        if resp.status_code != 200:
            return AqueductClientResponse(
                result="failed", message=f"Upload failed {HTTPStatus(resp.status_code).name}"
            )
        logging.info("Successfully uploaded file {files}")
        return AqueductClientResponse(result="success", message="File uploaded successfully")

    def download_file(
        self, experiment_uuid: UUID, file_name: str, destination_dir: str
    ) -> AqueductClientResponse:
        """
        Download file from a specific experiment.

        Args:
            experiment_uuid: The ID of the experiment.
            file_id: The ID of the file to be downloaded.
            destination: The local path where the downloaded file will be saved.

        Returns:
            Operation results object.

        """
        download_url: str = f"{self.url}/files/{experiment_uuid}/{file_name}"
        destination = f"{destination_dir}/{file_name}"

        try:
            with open(destination, "wb") as download_file:
                with stream("GET", download_url, timeout=self.timeout) as response:
                    total = int(response.headers["Content-Length"])
                    with tqdm(
                        total=total, unit_scale=True, unit_divisor=1024, unit="B"
                    ) as progress:
                        num_bytes_downloaded = response.num_bytes_downloaded
                        for chunk in response.iter_bytes():
                            download_file.write(chunk)
                            progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                            num_bytes_downloaded = response.num_bytes_downloaded

        except InterruptedDownloadException as exception:
            return AqueductClientResponse(result="failed", message=exception.message)

        except WriteTimeout as exception:
            return AqueductClientResponse(
                result="failed", message=f"Timeout error for file download {exception}"
            )

        return AqueductClientResponse(result="success", message=f"File downloaded to {destination}")

    def get_tags(self, limit: int, offset: int, dangling: bool = True) -> TagsData:
        """
        Get a list of existing tags

        Args:
        - limit (int): Number of tags to be fetched
        - offset (offset): Number of tags to skip
        - dangling (bool): If tags not linked to any experiment should be included or not

        Returns:
        List[str]: A list of all existing tags
        """
        if limit <= 0:
            raise ValueError("Limit cannot be 0")

        tags = self._session.execute(
            get_all_tags_query,
            variable_values={"limit": limit, "offset": offset, "dangling": dangling},
        )

        tags_obj = TagsData.from_dict(tags["tags"])  # pylint: disable=unsubscriptable-object
        logging.info("Fetched %s tags, total %s tags", len(tags_obj.tags), tags_obj.total_count)
        return tags_obj
