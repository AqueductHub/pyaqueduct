""" The module contains classes representing interface with plugins. """

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from pyaqueduct.client import AqueductClient
from pyaqueduct.client.plugin_types import (PluginExecutionResultData,
                                            PluginFunctionData,
                                            PluginParameterData)


class PluginExecutionResult(BaseModel):
    """Class representing result of plugin execution"""

    returnCode: int
    stdout: str
    stderr: str
    logExperiment: str
    logFile: str

    def __init__(self, result_data: PluginExecutionResultData):
        super().__init__(**result_data.model_dump())


class PluginParameter(BaseModel):
    """Plugin parameter class"""

    name: str
    displayName: Optional[str]
    description: Optional[str]
    dataType: str
    defaultValue: Optional[str]
    options: Optional[List[str]]

    def __init__(self, parameter_data: PluginParameterData):
        super().__init__(**parameter_data.model_dump())


class PluginFunction(BaseModel):
    """Plugin function representation"""

    parameters: List[PluginParameter]
    data: PluginFunctionData
    plugin: Plugin = None

    _client: AqueductClient = None

    def __init__(
        self,
        plugin: Plugin,
        function_data: PluginFunction,
        client: AqueductClient,
    ):
        super().__init__(plugin=plugin, data=function_data, parameters=[])
        self._client = client
        for parameter in function_data.parameters:
            self.parameters.append(PluginParameter(parameter))

    def execute(self, parameters: Dict[str, Any]) -> PluginExecutionResult:
        """Execute a plugin function on a server.

        Args:
            parameters: dictionary of parameters to pass to a plugin.

        Returns:
            result of plugin execution on server. `returnCode==0` corresponds to success.
        """
        result = self._client.execute_plugin_function(
            plugin=self.plugin.name,
            function=self.data.name,
            params=parameters,
        )
        return PluginExecutionResult(result)


class Plugin(BaseModel):
    """Class represents a plugin as a collection of functions."""

    name: str
    description: Optional[str]
    authors: str

    functions: List[PluginFunction]

    def __init__(self, name: str, description: Optional[str],
                 authors: str, functions: List[PluginFunctionData],
                 client: AqueductClient):
        super().__init__(name=name, description=description,
                         authors=authors, functions=[])
        for function in functions:
            self.functions.append(PluginFunction(self, function, client))
