""" The module contains classes representing interface with plugins. """

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from pyaqueduct.client import AqueductClient
from pyaqueduct.client.plugin_types import (PluginExecutionResultData,
                                            PluginFunctionData,
                                            PluginParameterData)


class PluginFunction(BaseModel):
    """Plugin function representation"""

    parameters: List[PluginParameterData]
    data: PluginFunctionData
    plugin: Plugin = None

    _client: AqueductClient = None

    def __init__(
        self,
        plugin: Plugin,
        function_data: PluginFunction,
        client: AqueductClient,
    ):
        super().__init__(plugin=plugin, data=function_data, parameters=function_data.parameters)
        self._client = client

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
