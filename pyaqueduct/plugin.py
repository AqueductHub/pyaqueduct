""" The module contains classes representing interface with plugins. """

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pyaqueduct.client import AqueductClient
from pyaqueduct.client.plugin_types import (PluginData,
                                            PluginExecutionResultData,
                                            PluginFunctionData,
                                            PluginParameterData)


class PluginExecutionResult(PluginExecutionResultData):
    """Class representing result of plugin execution"""


class PluginParameter(PluginParameterData):
    """Plugin parameter class"""


class PluginFunction(PluginFunctionData):
    """Plugin function representation"""

    parameters: List[PluginParameter]
    plugin: Optional[Plugin] = None

    _client: Optional[AqueductClient] = None

    # TODO: may require removal from autodocs
    # if used together with sphinx
    # see: https://stackoverflow.com/q/28224554
    def set_client(self, client: AqueductClient):
        """Sets the instance of the connection client object"""
        self._client = client

    def execute(self, parameters: Dict[str, Any]) -> PluginExecutionResult:
        """Execute a plugin function on a server.

        Args:
            parameters: dictionary of parameters to pass to a plugin.

        Raises:
            AttributeError: client connection should be initialised before this call.

        Returns:
            result of plugin execution on server. `returnCode==0` corresponds to success.
        """
        if self._client is None:
            raise AttributeError(
                "Field `_client` should have been initialised, but it is None."
            )
        result = self._client.execute_plugin_function(
            plugin=self.plugin.name,
            function=self.name,
            params=parameters,
        )
        return PluginExecutionResult(**result.model_dump())


class Plugin(PluginData):
    """Class represents a plugin as a collection of functions."""

    functions: List[PluginFunction]

    @staticmethod
    def from_data(data: PluginData, client: AqueductClient):
        """Initialise the object given a dictionary obtained from a server."""

        result = Plugin(**data.model_dump())
        for func in result.functions:
            func.plugin = result
            func.set_client(client)
        return result
