""" The module contains classes to represent task-related responses from the server. """

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from pyaqueduct.client.experiment_types import ExperimentData
from pyaqueduct.client.extension_types import ExtensionParameterData


class ParameterData(BaseModel):
    """Definition for task parameters"""

    key: ExtensionParameterData
    value: str


class TaskData(BaseModel):
    """Parameter definition for a task."""

    taskId: UUID
    taskStatus: str
    resultCode: str
    extensionName: str
    actionName: str
    createdBy: str
    receivedAt: datetime
    endedAt: datetime
    stdOut: str
    stdErr: str
    experiment: ExperimentData

    @classmethod
    def from_dict(cls, data: dict) -> TaskData:
        """Composes an object from a server response.

        Args:
            data: server response.

        Returns:
            Object populated with server response data.
        """
        return TaskData(**data)


class TasksData(BaseModel):
    """Parameter definition for tasks"""

    tasks: List[TaskData]
    tasksCount: int

    @classmethod
    def from_dict(cls, data: dict) -> TasksData:
        """Composes an object from a server response

        Args:
            data: server response

        Returns:
            Object populated with server response data
        """
        return TasksData(**data)
