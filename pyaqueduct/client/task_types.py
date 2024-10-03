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

    task_id: UUID
    task_status: str
    result_code: int
    extension_name: str
    action_name: str
    created_by: str
    received_at: datetime
    ended_at: datetime
    std_out: str
    std_err: str
    experiment: ExperimentData

    @classmethod
    def from_dict(cls, data: dict) -> TaskData:
        """Composes an object from a server response.

        Args:
            data: server response.

        Returns:
            Object populated with server response data.
        """
        from json import dumps
        print(dumps(data, indent=4))
        return cls(
            task_id=UUID(data["taskId"]),
            task_status=data["taskStatus"],
            result_code=data["resultCode"],
            extension_name=data["extensionName"],
            action_name=data["actionName"],
            created_by=data["createdBy"],
            received_at=data["receivedAt"],
            ended_at=data["endedAt"],
            std_out=data["stdOut"],
            std_err=data["stdErr"],
            experiment=ExperimentData.from_dict(data["experiment"])
        )


class TasksData(BaseModel):
    """Parameter definition for tasks"""

    tasks: List[TaskData]
    total_count: int

    @classmethod
    def from_dict(cls, data: dict) -> TasksData:
        """Composes an object from a server response

        Args:
            data: server response

        Returns:
            Object populated with server response data
        """
    @classmethod
    def from_dict(cls, data):
        """Convert tag data class to a dictionary"""
        return cls(
            tasks=[
                TaskData.from_dict(task_data) for task_data in data["tasksData"]
            ],
            total_count=data["totalTasksCount"],
        )

