"""Aqueduct client module to communicate with the server instance."""

from pyaqueduct.client.client import AqueductClient
from pyaqueduct.client.experiment_types import ExperimentData, ExperimentFile, ExperimentsInfo
from pyaqueduct.client.plugin_types import (
    PluginData, PluginFunctionData, PluginExecutionResultData, PluginParameterData)

__all__ = ["AqueductClient", "ExperimentData", "ExperimentFile", "ExperimentsInfo",
           "PluginData", "PluginFunctionData", "PluginExecutionResultData", "PluginParameterData"]
