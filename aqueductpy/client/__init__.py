"""Aqueduct client module to communicate with the server instance."""

from aqueductpy.client.client import AqueductClient
from aqueductpy.client.types import ExperimentData, ExperimentFile, ExperimentsInfo

__all__ = ["AqueductClient", "ExperimentData", "ExperimentFile", "ExperimentsInfo"]
