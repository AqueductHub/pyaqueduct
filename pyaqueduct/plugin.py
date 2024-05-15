""" The module contains classes representing interface with plugins. Plugin
list may be retrieved from the server using api function `API.get_plugins().
Each plugin may have one or more functions. Each function has a list of expected
parameters."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from pyaqueduct.client import AqueductClient
from pyaqueduct.client.plugin_types import (PluginExecutionResultData,
                                            PluginFunctionData,
                                            PluginParameterData)


class PluginFunction(BaseModel):
    """Plugin function representation. Contains an execution method
    which trigger pluhin function execution on the side of Aqueduct server."""

    parameters: List[PluginParameterData]
    """List of parameters which plugin function expects to accept."""

    data: PluginFunctionData
    plugin: Plugin = None
    """Plugin, which this function belongs to."""

    _client: AqueductClient = None

    def __init__(
        self,
        plugin: Plugin,
        function_data: PluginFunction,
        client: AqueductClient,
    ):
        super().__init__(plugin=plugin, data=function_data, parameters=function_data.parameters)
        self._client = client

    @property
    def name(self) -> str:
        """Plugin function name. Unique inside a plugin."""
        return self.data.name

    @property
    def description(self) -> str:
        """Detailed description of the plugin function."""
        return self.data.description

    @property
    def experiment_variable_name(self) -> str:
        """Name of the variable which is used to define a default experiment.
        This experiment will be used to save logs and validate variables
        of `file` type."""
        return self.data.experimentVariableName

    def execute(self, parameters: Dict[str, Any]) -> PluginExecutionResultData:
        """Execute a plugin function on a server.

        Args:
            parameters: dictionary of parameters to pass to a plugin.

        Returns:
            result of plugin execution on server. `returnCode==0` corresponds to success.
        """
        return self._client.execute_plugin_function(
            plugin=self.plugin.name,
            function=self.data.name,
            params=parameters,
        )


class Plugin(BaseModel):
    """Class represents a plugin as a collection of functions."""

    name: str
    """Plugin name. Unique name within a server"""

    description: Optional[str]
    """Description of plugin scope and overview of its functions."""

    authors: str
    """Authors of the plugin."""

    functions: List[PluginFunction]

    def __init__(self, name: str, description: Optional[str],
                 authors: str, functions: List[PluginFunctionData],
                 client: AqueductClient):
        super().__init__(name=name, description=description,
                         authors=authors, functions=[])
        for function in functions:
            self.functions.append(PluginFunction(self, function, client))
