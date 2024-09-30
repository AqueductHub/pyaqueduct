"""Aqueduct client class to enable experiment based operations."""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from gql import Client
from gql.client import SyncClientSession
from gql.transport import exceptions as gql_exceptions
from gql.transport.httpx import HTTPXTransport
from graphql import DocumentNode
from httpx import TransportError, codes, post, stream
from pydantic import BaseModel, HttpUrl, PrivateAttr
from tqdm import tqdm

from pyaqueduct.client.experiment_types import ExperimentData, ExperimentsInfo, TagsData
from pyaqueduct.client.extension_types import (
    ExtensionCancelResultData,
    ExtensionData,
    ExtensionExecutionResultData,
)
from pyaqueduct.client.task_types import TaskData
from pyaqueduct.exceptions import (
    FileDownloadError,
    FileRemovalError,
    FileUploadError,
    ForbiddenError,
    RemoteOperationError,
    UnAuthorizedError,
)
from pyaqueduct.schemas.mutations import (
    add_tags_to_experiment_mutation,
    cancel_task_mutation,
    create_experiment_mutation,
    execute_extension_action_mutation,
    remove_experiment_mutation,
    remove_tag_from_experiment_mutation,
    update_experiment_mutation,
)
from pyaqueduct.schemas.queries import (
    get_all_extensions_query,
    get_all_tags_query,
    get_experiment_query,
    get_experiments_query,
    get_task_query,
    get_tasks_query,
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

    def fetch_response(self, operation: DocumentNode, variable_values: Dict) -> Dict[str, Any]:
        """
        Send query or mutation request to the server.

        Args:
            operation: Query or mutation schema.
            variable_values: Values for the params to be sent in the request.

        Returns:
            A JSON object
        """
        try:
            data = self._gql_client.execute(
                operation,
                variable_values=variable_values,
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error
        return data

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

        data = self.fetch_response(
            create_experiment_mutation,
            {"title": title, "description": description, "tags": tags or []},
        )
        experiment_obj = ExperimentData.from_dict(data["createExperiment"])
        logging.info("Created experiment - %s - %s", experiment_obj.uuid, experiment_obj.title)
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
        data = self.fetch_response(
            update_experiment_mutation,
            {
                "uuid": str(experiment_uuid),
                "title": title,
                "description": description,
            },
        )
        experiment_obj = ExperimentData.from_dict(data["updateExperiment"])
        logging.info("Updated experiment - %s", experiment_obj.uuid)
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
            title: Perform search on experiments through their title and EID.
            tags: Get experiments that have these tags.
            start_date: Start datetime to filter experiments (timezone aware).
            end_date: End datetime to filter experiments to (timezone aware).

        Returns:
            List of experiments with filters applied.

        """
        data = self.fetch_response(
            get_experiments_query,
            {
                "limit": limit,
                "offset": offset,
                "title": title,
                "startDate": start_datetime.isoformat() if start_datetime else None,
                "endDate": end_datetime.isoformat() if end_datetime else None,
                "tags": tags,
            },
        )
        experiments_obj = ExperimentsInfo.from_dict(data["experiments"])
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
        data = self.fetch_response(
            get_experiment_query,
            {"type": "UUID", "value": str(experiment_uuid)},
        )
        experiment_obj = ExperimentData.from_dict(data["experiment"])
        logging.info("Fetched experiment - %s", experiment_obj.title)
        return experiment_obj

    def get_experiment_by_eid(self, eid: str) -> ExperimentData:
        """
        Get an experiment by its EID.

        Args:
            EID: Experiment's EID.

        Returns:
            Updated experiment.

        """
        data = self.fetch_response(
            get_experiment_query,
            {"type": "EID", "value": eid},
        )
        experiment_obj = ExperimentData.from_dict(data["experiment"])
        logging.info("Fetched experiment - %s", experiment_obj.title)
        return experiment_obj

    def add_tags_to_experiment(self, experiment_uuid: UUID, tags: List[str]) -> ExperimentData:
        """
        Add tags to an experiment.

        Args:
            experiment_uuid: UUID of experiment.
            tags: List of tags to be added to experiment.

        Returns:
            Updated experiment.

        """
        data = self.fetch_response(
            add_tags_to_experiment_mutation,
            {"uuid": str(experiment_uuid), "tags": tags},
        )
        experiment_obj = ExperimentData.from_dict(data["addTagsToExperiment"])
        logging.info("Added tags %s to experiment <%s>", tags, experiment_obj.title)
        return experiment_obj

    def remove_experiment(self, experiment_uuid: UUID) -> None:
        """
        Remove experiment from the database. It removes the experiments files as well.

        Args:
            experiment_uuid: UUID of experiment.

        """
        self.fetch_response(
            remove_experiment_mutation,
            {"uuid": str(experiment_uuid)},
        )

    def remove_tag_from_experiment(self, experiment_uuid: UUID, tag: str) -> ExperimentData:
        """
        Remove a tag from an experiment

        Args:
            experiment_uuid (UUID): UUID of experiment frin which tag has to be removed
            tag (str): Tag to be removed from experiment

        Returns:
            Experiment: Experiment having tag removed
        """
        data = self.fetch_response(
            remove_tag_from_experiment_mutation,
            {"uuid": str(experiment_uuid), "tag": tag},
        )

        experiment_obj = ExperimentData.from_dict(data["removeTagFromExperiment"])
        logging.info("Removed tag %s from experiment <%s>", tag, experiment_obj.title)
        return experiment_obj

    def remove_files_from_experiment(self, experiment_uuid: UUID, files: List[str]) -> None:
        """
        Remove files from an experiment

        Args:
            experiment_uuid: UUID of experiment for which files has to be removed from.
            files: List of file names to be removed.

        """

        remove_url = f"{self.url}/files/{experiment_uuid}/delete_files"
        try:
            response = post(remove_url, timeout=self.timeout, json={"file_list": files})
        except TransportError as error:
            raise FileRemovalError("Couldn't remove files due to server error.") from error

        process_response_common(codes(response.status_code))

        logging.info("Successfully removed files %s from experiment.", files)

    def get_tags(self, limit: int, offset: int, dangling: bool = True) -> TagsData:
        """
        Get a list of existing tags

        Args:
            limit (int): Number of tags to be fetched
            offset (offset): Number of tags to skip
            dangling (bool): If tags not linked to any experiment should be included or not

        Returns:
        List[str]: A list of all existing tags
        """
        data = self.fetch_response(
            get_all_tags_query,
            {"limit": limit, "offset": offset, "dangling": dangling},
        )
        tags_obj = TagsData.from_dict(data["tags"])
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

    def get_extensions(self) -> List[ExtensionData]:
        """Get the list of extensions from the server.

        Returns:
            List of extension objects.
        """
        try:
            extensions_response = self._gql_client.execute(
                get_all_extensions_query,
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occurred in the remote operation."
            ) from error

        extensions_list = list(
            map(
                ExtensionData.from_dict,
                extensions_response["extensions"],
            )
        )
        logging.info("Fetched %s extensions", len(extensions_list))
        return extensions_list

    def execute_extension_action(
        self, extension: str, action: str, params: Dict[str, Any]
    ) -> ExtensionExecutionResultData:
        """Executes extension action on a server.

        Args:
            extension: extension name.
            action: action name within an extension.
            params: dictionary with parameters passed to an extension.

        Raises:
            RemoteOperationError: Communication error.

        Returns:
            Extension execution result, `returnCode==0` corresponds to success.
        """
        try:
            params_list = [[k, str(v)] for k, v in params.items()]
            extension_result = self._gql_client.execute(
                execute_extension_action_mutation,
                variable_values={
                    "extension": extension,
                    "action": action,
                    "params": params_list,
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

        result = ExtensionExecutionResultData.from_dict(extension_result["executeExtension"])
        logging.info(
            "Executed a %s / %s extension action with result code %d",
            extension,
            action,
            result.returnCode,
        )
        return result

    def get_task(self, task_id: str) -> TaskData:
        """Get details for a submitted taks

        Args:
            task_id: Task identifier
        """
        try:
            task_result = self._gql_client.execute(
                get_task_query, variable_values={"taskId": task_id}
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occoured in the remote operation"
            )

        result = TaskData.from_dict(task_result["task"])
        return result

    def get_tasks(
        self,
        limit: int,
        offset: int,
        extensionName: Optional[str] = None,
        experimentUuid: Optional[str] = None,
        actionName: Optional[str] = None,
        username: Optional[str] = None,
        startDate: Optional[datetime] = None,
        endDate: Optional[datetime] = None,
    ) -> TaskData:
        """Get details for a submitted taks

        Args:
            limit: int,
            offset: int,
            extensionName: Optional[str] = None,
            experimentUuid: Optional[str] = None,
            actionName: Optional[str] = None,
            username: Optional[str] = None,
            startDate: Optional[DateTime] = None,
            endDate: Optional[DateTime] = None,

        """
        try:
            task_result = self._gql_client.execute(
                get_tasks_query,
                variable_values={
                    "limit": limit,
                    "offset": offset,
                    "extensionName": extensionName,
                    "experimentUuid": experimentUuid,
                    "actionName": actionName,
                    "username": username,
                    "startDate": startDate,
                    "endDate": endDate,
                },
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occoured in the remote operation"
            )

        result = TaskData.from_dict(task_result["task"])
        return result

    def cancel_task(self, task_id: str) -> ExtensionCancelResultData:
        """Stops and cancels task running in Celery

        Args:
            task_id: Task identifier
        """
        try:
            revoke_result = self._gql_client.execute(
                cancel_task_mutation,
                variable_values={"taskId": task_id},
            )
        except gql_exceptions.TransportServerError as error:
            if error.code:
                process_response_common(codes(error.code))
            raise
        except gql_exceptions.TransportQueryError as error:
            raise RemoteOperationError(
                error.errors if error.errors else "Unknown error occoured in the remote operation"
            )

        result = ExtensionCancelResultData.from_dict(revoke_result["cancelTask"])
        return result
