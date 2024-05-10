""" The module contains classes to represent plugin-related responses from the server. """

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class PluginParameterData(BaseModel):
    """Parameter definition for a plugin function."""

    name: str
    displayName: Optional[str]
    description: Optional[str]
    dataType: str
    defaultValue: Optional[str]
    options: Optional[List[str]]


class PluginFunctionData(BaseModel):
    """Executable plugin function."""

    name: str
    description: str
    experimentVariableName: str
    parameters: List[PluginParameterData]


class PluginData(BaseModel):
    """Dataclass for defining a plugin"""

    name: str
    description: Optional[str]
    authors: str
    functions: List[PluginFunctionData]

    @classmethod
    def from_dict(cls, data: dict) -> PluginData:
        """Composes an object from a server response.

        Args:
            data: server response.

        Returns:
            Object populated with server response data.
        """
        return PluginData(**data)


class PluginExecutionResultData(BaseModel):
    """Results of plugin execution"""

    returnCode: int
    stdout: str
    stderr: str
    logExperiment: str
    logFile: str

    @classmethod
    def from_dict(cls, data: dict) -> PluginExecutionResultData:
        """Composes an object from a server response.

        Args:
            data: server response.

        Returns:
            Object populated with server response data.
        """
        return PluginExecutionResultData(**data)
