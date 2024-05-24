"""Aqueduct client module to communicate with the server instance."""

from pyaqueduct.client.client import AqueductClient
from pyaqueduct.client.experiment_types import ExperimentData, ExperimentFile, ExperimentsInfo
from pyaqueduct.client.extension_types import (
    ExtensionData, ExtensionActionData, ExtensionExecutionResultData, ExtensionParameterData)

__all__ = ["AqueductClient", "ExperimentData", "ExperimentFile", "ExperimentsInfo",
           "ExtensionData", "ExtensionActionData", "ExtensionExecutionResultData", 
           "ExtensionParameterData"]
