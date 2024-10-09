"""Task module."""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, PrivateAttr

from pyaqueduct.client import AqueductClient
from pyaqueduct.client.experiment_types import ExperimentData
from pyaqueduct.client.extension_types import ExtensionCancelResultData
from pyaqueduct.client.task_types import ParameterData


class Task(BaseModel):
    """Task representation. Contains all data and metadata about Aqueduct Task"""

    _client: AqueductClient = PrivateAttr()
    "Client object reference."

    uuid: UUID
    """UUID for task."""

    created_by: str
    """User who executed the task."""

    received_at: datetime
    """Time at which action was executed."""

    experiment: ExperimentData
    """Experiment to which task belongs"""

    extension_name: str
    """Name of extension to which action belongs."""

    action_name: str
    """Name of action called."""

    parameters: List[ParameterData]
    """List of parameters with key and value passed to action"""

    def __init__(self, client: AqueductClient, uuid: str):
        # Call parent constructor for Pydantic validation
        task_data = client.get_task(uuid)

        parameters = [
            param if isinstance(param, ParameterData) else ParameterData.from_dict(param)
            for param in task_data.parameters
        ]
        super().__init__(
            uuid=task_data.task_id,
            extension_name=task_data.extension_name,
            action_name=task_data.action_name,
            created_by=task_data.created_by,
            received_at=task_data.received_at,
            experiment=task_data.experiment,
            parameters=parameters,
        )

        self._client = client

    @property
    def task_status(self) -> str:
        """Status of task."""
        return self._client.get_task(str(self.uuid)).task_status

    @property
    def result_code(self) -> int:
        """Result code for executed process."""
        return self._client.get_task(str(self.uuid)).result_code

    @property
    def ended_at(self) -> datetime:
        """Time at which execution of task was completed."""
        return self._client.get_task(str(self.uuid)).ended_at

    @property
    def std_out(self) -> str:
        """Output string of task execution."""
        return self._client.get_task(str(self.uuid)).std_out

    @property
    def std_err(self) -> str:
        """Errors propagated during task execution."""
        return self._client.get_task(str(self.uuid)).std_err

    def cancel_task(self) -> ExtensionCancelResultData:
        """Cancel or revoke current executing task"""
        result = self._client.cancel_task(str(self.uuid))
        return result
