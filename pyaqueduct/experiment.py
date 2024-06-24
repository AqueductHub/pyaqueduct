"""Experiment module."""

from __future__ import annotations

from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from pydantic import BaseModel, validate_call

from pyaqueduct.client import AqueductClient


class Experiment(BaseModel):
    """Experiment model."""

    _client: AqueductClient
    "Client object reference."
    uuid: UUID
    "UUID of the experiment. This is an internal experiment identifier in the database"
    eid: str
    "EID of the experiment. User-readable identifier, it is unique within one Aqueduct installation"
    created_at: datetime
    "Creation datetime of the experiment."

    def __init__(self, uuid: UUID, eid: str, created_at: datetime, client: AqueductClient, **data):
        super().__init__(uuid=uuid, eid=eid, created_at=created_at, **data)
        self._client = client

    @property
    def title(self) -> str:
        """Get title of experiment."""
        return self._client.get_experiment(experiment_uuid=self.uuid).title

    @title.setter
    @validate_call
    def title(self, value: str) -> None:
        """Set title of experiment.

        Args:
            value: New title.

        """
        self._client.update_experiment(experiment_uuid=self.uuid, title=value)

    @property
    def description(self) -> str:
        """Get description of experiment."""
        return self._client.get_experiment(self.uuid).description

    @description.setter
    @validate_call
    def description(self, value: str) -> None:
        """Set description of experiment.

        Args:
            value: New description.

        """
        self._client.update_experiment(experiment_uuid=self.uuid, description=value)

    @property
    def tags(self) -> List[str]:
        """Gets tags of experiment."""
        return self._client.get_experiment(self.uuid).tags

    @validate_call
    def add_tags(self, tags: List[str]) -> None:
        """Add new tags to experiment.

        Args:
            tags: List of tags to be added to the experiment.

        """
        self._client.add_tags_to_experiment(experiment_uuid=self.uuid, tags=tags)

    @validate_call
    def remove_tag(self, tag: str) -> None:
        """Remove tag from experiment."""
        self._client.remove_tag_from_experiment(experiment_uuid=self.uuid, tag=tag)

    @property
    def files(self) -> List[Tuple[str, datetime]]:
        """Get file names of expriment."""
        return [
            (item.name, item.modified_at) for item in self._client.get_experiment(self.uuid).files
        ]

    @validate_call
    def download_file(self, file_name: str, destination_dir: str) -> None:
        """Download the specified file of experiment."""
        self._client.download_file(self.uuid, file_name=file_name, destination_dir=destination_dir)

    @validate_call
    def upload_file(self, file: str) -> None:
        """Upload the specified file to experiment."""
        self._client.upload_file(self.uuid, file=file)

    @property
    def updated_at(self) -> datetime:
        """Get last updated datetime of the experiment."""
        return self._client.get_experiment(self.uuid).updated_at
