"""Dataclasses for experiment and it's components"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass
class ExperimentFile:
    """Dataclass for experiment file"""

    name: str
    path: str
    modified_at: datetime

    @classmethod
    def from_dict(cls, data):
        """Convert experiment file object to dictionary"""
        return cls(
            name=data["name"],
            path=data["path"],
            modified_at=datetime.fromisoformat(data["modifiedAt"]),
        )


@dataclass
class ExperimentData:
    """Dataclass for experiment"""

    id: UUID  # pylint: disable=invalid-name
    title: str
    description: str
    alias: str
    created_at: datetime
    updated_at: datetime
    tags: List[str] = field(default_factory=list)
    files: List[ExperimentFile] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data):
        """Convert experiment object to dictionary"""
        return cls(
            id=UUID(data["id"]),
            title=data["title"],
            description=data["description"],
            tags=data["tags"],
            alias=data["alias"],
            files=[ExperimentFile.from_dict(file_data) for file_data in data["files"]],
            created_at=datetime.fromisoformat(data["createdAt"]),
            updated_at=datetime.fromisoformat(data["updatedAt"]),
        )


@dataclass
class ExperimentsInfo:
    """Dataclass for experiment info"""

    experiments: List[ExperimentData]
    total_count: int

    @classmethod
    def from_dict(cls, data):
        """Convert experiment info object to dictionary"""
        return cls(
            experiments=[
                ExperimentData.from_dict(exp_data) for exp_data in data["experimentsData"]
            ],
            total_count=data["totalExperimentsCount"],
        )


@dataclass
class TagsData:
    """Dataclass for definition of tag"""

    tags: List[str]
    total_count: int

    @classmethod
    def from_dict(cls, data):
        """Convert tag data class to a dictionary"""
        return cls(tags=data["tagsData"], total_count=data["totalTagsCount"])
