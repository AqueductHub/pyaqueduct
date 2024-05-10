"""Aqueduct client class to enable experiment based operations."""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from gql import Client
from gql.client import SyncClientSession
from gql.transport import exceptions as gql_exceptions
from gql.transport.httpx import HTTPXTransport
from httpx import TransportError, codes, post, stream
from pydantic import BaseModel, HttpUrl, PrivateAttr
from tqdm import tqdm

from pyaqueduct.client.types import ExperimentData, ExperimentsInfo, TagsData
from pyaqueduct.exceptions import (
    FileDownloadError,
    FileUploadError,
    ForbiddenError,
    RemoteOperationError,
    UnAuthorizedError,
)
from pyaqueduct.schemas.mutations import (
    add_tag_to_experiment_mutation,
    create_experiment_mutation,
    remove_experiment_mutation,
    remove_tag_from_experiment_mutation,
    update_experiment_mutation,
)
from pyaqueduct.schemas.queries import (
    get_all_tags_query,
    get_experiment_query,
    get_experiments_query,
)


def process_response_common(code: codes) -> None:
    """Process common HTTP return codes."""
    if code is codes.OK:
        return

    if code is codes.FORBIDDEN:
        raise ForbiddenError("Operation is not allowed for the current user.") from None

    if code is codes.UNAUTHORIZED:
        raise UnAuthorizedError("API token couldn't be verified or is missing.") from None

    raise RemoteOperationError("Remove operation failed.")


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
    _headers: Dict[str, str] = PrivateAttr()

    def __init__(self, url: str, timeout: float, api_token: Optional[str] = None):
        """
        Args:
            url: URL of the Aqueduct server endpoint.
            timeout: Response timeout in seconds.

        """
        super().__init__(url=url, timeout=timeout)
        self._headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}

        self._gql_client = Client(
            transport=HTTPXTransport(
                url=f"{url}/graphql", timeout=self.timeout, headers=self._headers
            )
        )

    def create_experiment(
        self, title: str, description: str, tags: Optional[List[str]] = None
    ) -> ExperimentData:
        """
        Create an experiment with title, description and list of tags.

        Args:
            title: Title of experiment.
            description: Description of experiment.
            tags: List of tags to be assigned to experiment.

        Returns:
            Experiment object.
        """
        try:
            experiment = self._gql_client.execute(
                create_experiment_mutation,
                variable_values={"title": title, "description": description, "tags": tags or []},
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

        experiment_obj = ExperimentData.from_dict(
            experiment["createExperiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Created experiment - %s - %s", experiment_obj.id, experiment_obj.title)
        return experiment_obj

    def update_experiment(
        self, experiment_uuid: UUID, title: Optional[str] = None, description: Optional[str] = None
    ) -> ExperimentData:
        """
        Update title or description or both for experiment.

        Args:
            experiment_uuid: UUID of experiment.
            title: New title of experiment.
            description: New description of experiment.

        Returns:
            Experiment object.

        """
        if title and title == "":
            raise ValueError("Title cannot be an empty string")

        if description and description == "":
            raise ValueError("Description cannot be an empty string")

        try:
            experiment = self._gql_client.execute(
                update_experiment_mutation,
                variable_values={
                    "experimentId": str(experiment_uuid),
                    "title": title,
                    "description": description,
                },
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

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
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
    ) -> ExperimentsInfo:
        """
        Get a list of experiments

        Args:
            limit: Pagination field, number of experiments to be fetched.
            offset: Pagination field, number of experiments to skip.
            title: Perform search on experiments through their title and alias.
            tags: Get experiments that have these tags.
            start_date: Start datetime to filter experiments (timezone aware).
            end_date: End datetime to filter experiments to (timezone aware).

        Returns:
            List of experiments with filters applied.

        """
        if limit <= 0:
            raise ValueError("Limit should be a positive number")

        try:
            experiments = self._gql_client.execute(
                get_experiments_query,
                variable_values={
                    "limit": limit,
                    "offset": offset,
                    "title": title,
                    "startDate": start_datetime.isoformat() if start_datetime else None,
                    "endDate": end_datetime.isoformat() if end_datetime else None,
                    "tags": tags,
                },
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

        experiments_obj = ExperimentsInfo.from_dict(
            experiments["experiments"]  # pylint: disable=unsubscriptable-object
        )
        logging.info(
            "Fetched %s experiments, total %s experiments",
            len(experiments_obj.experiments),
            experiments_obj.total_count,
        )
        return experiments_obj

    def get_experiment(self, experiment_uuid: UUID) -> ExperimentData:
        """
        Get an Experiment by UUID.

        Args:
            experiment_uuid: UUID of experiment.

        Returns:
            Experiment object.

        """
        try:
            experiment = self._gql_client.execute(
                get_experiment_query,
                variable_values={"type": "UUID", "value": str(experiment_uuid)},
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

        experiment_obj = ExperimentData.from_dict(
            experiment["experiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Fetched experiment - %s", experiment_obj.title)
        return experiment_obj

    def get_experiment_by_alias(self, alias: str) -> ExperimentData:
        """
        Get an Experiment by Alias.

        Args:
            alias: Experiment's alias.

        Returns:
            Updated experiment.

        """
        try:
            experiment = self._gql_client.execute(
                get_experiment_query, variable_values={"type": "ALIAS", "value": alias}
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

        experiment_obj = ExperimentData.from_dict(
            experiment["experiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Fetched experiment - %s", experiment_obj.title)
        return experiment_obj

    def add_tag_to_experiment(self, experiment_uuid: UUID, tag: str) -> ExperimentData:
        """
        Add a tag to an experiment

        Args:
            experiment_uuid: UUID of experiment.
            tag: Tag to be added to experiment.

        Returns:
            Updated experiment.

        """
        try:
            experiment = self._gql_client.execute(
                add_tag_to_experiment_mutation,
                variable_values={"experimentId": str(experiment_uuid), "tag": tag},
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

        experiment_obj = ExperimentData.from_dict(
            experiment["addTagToExperiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Added tag %s to experiment <%s>", tag, experiment_obj.title)
        return experiment_obj

    def remove_experiment(self, experiment_uuid: UUID) -> None:
        """
        Remove experiment from the database. It removes the experiments files as well.

        Args:
            experiment_uuid: UUID of experiment.

        """
        try:
            self._gql_client.execute(
                remove_experiment_mutation,
                variable_values={"experimentId": str(experiment_uuid)},
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

    def remove_tag_from_experiment(self, experiment_uuid: UUID, tag: str) -> ExperimentData:
        """
        Remove a tag from an experiment

        Args:
        - experiment_uuid (UUID): UUID of experiment frin which tag has to be removed
        - tag (str): Tag to be removed from experiment

        Returns:
        Experiment: Experiment having tag removed
        """
        try:
            experiment = self._gql_client.execute(
                remove_tag_from_experiment_mutation,
                variable_values={"experimentId": str(experiment_uuid), "tag": tag},
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

        experiment_obj = ExperimentData.from_dict(
            experiment["removeTagFromExperiment"]  # pylint: disable=unsubscriptable-object
        )
        logging.info("Removed tag %s from experiment <%s>", tag, experiment_obj.title)
        return experiment_obj

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

        try:
            tags = self._gql_client.execute(
                get_all_tags_query,
                variable_values={"limit": limit, "offset": offset, "dangling": dangling},
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

        tags_obj = TagsData.from_dict(tags["tags"])  # pylint: disable=unsubscriptable-object
        logging.info("Fetched %s tags, total %s tags", len(tags_obj.tags), tags_obj.total_count)
        return tags_obj

    def upload_file(self, experiment_uuid: UUID, file: str) -> None:
        """
        Upload file to a specific experiment.

        Args:
            experiment_uuid : The ID of the experiment.
            file_path: The local path to the file to be uploaded.

        Returns:
            Operation results object.

        """

        headers = {"file_name": os.path.basename(file), **self._headers}

        upload_url = f"{self.url}/files/{str(experiment_uuid)}"
        with open(file, "rb") as files:
            try:
                response = post(
                    upload_url, headers=headers, timeout=self.timeout, files={"file": files}
                )
            except TransportError as error:
                raise FileUploadError(f"Couldn't upload {file} due to transport error.") from error

        process_response_common(codes(response.status_code))

        logging.info("Successfully uploaded file {files}")

    def download_file(self, experiment_uuid: UUID, file_name: str, destination_dir: str) -> None:
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
                with stream(
                    "GET", download_url, timeout=self.timeout, headers=self._headers
                ) as response:
                    total = int(response.headers["Content-Length"])
                    with tqdm(
                        total=total, unit_scale=True, unit_divisor=1024, unit="B"
                    ) as progress:
                        num_bytes_downloaded = response.num_bytes_downloaded
                        for chunk in response.iter_bytes():
                            download_file.write(chunk)
                            progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                            num_bytes_downloaded = response.num_bytes_downloaded

        except Exception as error:
            raise FileDownloadError(
                f"Couldn't download {file_name} due to transport error."
            ) from error
