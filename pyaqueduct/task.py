"""Task models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from pyaqueduct.client import AqueductClient
from pyaqueduct.client.experiment_types import ExperimentData


class Task(BaseModel):
    """Task representation. Contains all data and metadata about
    Aqueduct Task"""

    _client: AqueductClient
    "Client object reference."

    uuid: UUID
    """UUID for task."""

    extension_name: str
    """Name of extension to which action belongs."""

    action_name: str
    """Name of action called."""

    created_by: str
    """User who executed the task."""

    received_at: datetime
    """Time at which action was executed."""

    experiment: ExperimentData
    """Experiment to which task belongs"""

    def __init__(self, client: AqueductClient, task_id: str):
        self._client = client

        task_data = self._client.get_task(self.task_id)
        self.extension_name = task_data.extension_name
        self.action_name = task_data.action_name
        self.created_by = task_data.created_by
        self.received_at = task_data.received_at
        self.experiment = task_data.experiment

        super().__init__(task_id=task_id)

    @property
    def task_status(self) -> str:
        """Status of task."""
        return self._client.get_task(self.task_id).task_status

    @property
    def result_code(self) -> int:
        """Result code for executed process."""
        return self._client.get_task(self.task_id).result_code

    @property
    def ended_at(self) -> datetime:
        """Time at which execution of task was completed."""
        return self._client.get_task(self.task_id).ended_at

    @property
    def std_out(self) -> str:
        """Output string of task execution."""
        return self._client.get_task(self.task_id).std_out

    @property
    def std_err(self) -> str:
        """Errors propagated during task execution."""
        return self._client.get_task(self.task_id).std_err
