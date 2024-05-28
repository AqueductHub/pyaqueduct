""" The module contains classes to represent extension-related responses from the server. """

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class ExtensionParameterData(BaseModel):
    """Parameter definition for an extension action."""

    name: str
    displayName: Optional[str]
    description: Optional[str]
    dataType: str
    defaultValue: Optional[str]
    options: Optional[List[str]]


class ExtensionActionData(BaseModel):
    """Executable extension action."""

    name: str
    description: str
    experimentVariableName: str
    parameters: List[ExtensionParameterData]


class ExtensionData(BaseModel):
    """Dataclass for defining an extension"""

    name: str
    description: Optional[str]
    authors: str
    actions: List[ExtensionActionData]

    @classmethod
    def from_dict(cls, data: dict) -> ExtensionData:
        """Composes an object from a server response.

        Args:
            data: server response.

        Returns:
            Object populated with server response data.
        """
        return ExtensionData(**data)


class ExtensionExecutionResultData(BaseModel):
    """Results of extension execution"""

    returnCode: int
    stdout: str
    stderr: str
    logExperiment: str
    logFile: str

    @classmethod
    def from_dict(cls, data: dict) -> ExtensionExecutionResultData:
        """Composes an object from a server response.

        Args:
            data: server response.

        Returns:
            Object populated with server response data.
        """
        return ExtensionExecutionResultData(**data)
