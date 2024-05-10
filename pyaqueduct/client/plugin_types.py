from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class PluginParameterData(BaseModel):
    name: str
    displayName: Optional[str]
    description: Optional[str]
    dataType: str
    defaultValue: Optional[str]
    options: Optional[List[str]]


class PluginFunctionData(BaseModel):
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
        return PluginData(**data)


class PluginExecutionResultData(BaseModel):
    """Results of plugin execution """
    returnCode: int
    stdout: str
    stderr: str

    @classmethod
    def from_dict(cls, data: dict) -> PluginExecutionResultData:
        return PluginExecutionResultData(**data)
