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

    task_id: str
    """UUID for task."""

    extensionName: str
    """Name of extension to which action belongs."""

    actionName: str
    """Name of action called."""

    createdBy: str
    """User who executed the task."""

    receivedAt: datetime
    """Time at which action was executed."""

    experiment: ExperimentData
    """Experiment to which task belongs"""

    @property
    def taskStatus(self) -> str:
        """Status of task."""
        return self._client.get_task(self.task_id).taskStatus

    @property
    def resultCode(self) -> str:
        """Result code for executed process."""
        return self._client.get_task(self.task_id).resultCode

    @property
    def endedAt(self) -> datetime:
        """Time at which execution of task was completed."""
        return self._client.get_task(self.task_id).endedAt

    @property
    def stdOut(self) -> str:
        """Output string of task execution."""
        return self._client.get_task(self.task_id).stdOut

    @property
    def stdErr(self) -> str:
        """Errors propagated during task execution."""
        return self._client.get_task(self.task_id).stdErr

    def __init__(self, client: AqueductClient, task_id: str):
        self._client = client

        task_data = self._client.get_task(self.task_id)
        self.extensionName = task_data.extensionName
        self.actionName = task_data.actionName
        self.createdBy = task_data.createdBy
        self.receivedAt = task_data.receivedAt
        self.experiment = task_data.experiment

        super().__init__(task_id=task_id)
