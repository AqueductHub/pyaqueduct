from __future__ import annotations

from typing import Any, Dict, List, Optional

from pyaqueduct.client.plugin_types import (PluginData, PluginFunctionData,
                                            PluginParameterData)


class PluginParameter(PluginParameterData):
    """Plugin parameter class"""


class PluginFunction(PluginFunctionData):
    """Plugin function representation"""

    parameters: List[PluginParameter]
    plugin: Optional[Plugin] = None

    def execute(parameters: Dict[str, Any]):
        pass


class Plugin(PluginData):
    functions: List[PluginFunction]

    @staticmethod
    def from_data(data: PluginData):
        result = Plugin(**data.dict())
        for func in result.functions:
            func.plugin = result
        return result
