""" The module contains classes representing interface with extensions. Extension
list may be retrieved from the server using api method `API.get_extensions()`.
Each extension may have one or more actions. Each action has a list of expected
parameters."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from pyaqueduct.client import AqueductClient
from pyaqueduct.client.extension_types import (ExtensionExecutionResultData,
                                            ExtensionActionData,
                                            ExtensionParameterData)


class ExtensionAction(BaseModel):
    """Extension action representation. Contains an execution method
    which trigger extension action execution on the side of Aqueduct server."""

    parameters: List[ExtensionParameterData]
    """List of parameters which extension action expects to accept."""

    data: ExtensionActionData
    extension: Extension = None
    """Extension to which this action belongs."""

    _client: AqueductClient = None

    def __init__(
        self,
        extension: Extension,
        action_data: ExtensionAction,
        client: AqueductClient,
    ):
        super().__init__(extension=extension, data=action_data, parameters=action_data.parameters)
        self._client = client

    @property
    def name(self) -> str:
        """Extension action name. Unique inside an extension."""
        return self.data.name

    @property
    def description(self) -> str:
        """Detailed description of the extension action."""
        return self.data.description

    @property
    def experiment_variable_name(self) -> str:
        """Name of the variable which is used to define a default experiment.
        This experiment will be used to save logs and validate variables
        of `file` type."""
        return self.data.experimentVariableName

    def execute(self, parameters: Dict[str, Any]) -> ExtensionExecutionResultData:
        """Execute an extension action on a server.

        Args:
            parameters: dictionary of parameters to pass to an extension.

        Returns:
            result of extension execution on server. `returnCode==0` corresponds to success.
        """
        return self._client.execute_extension_action(
            extension=self.extension.name,
            action=self.data.name,
            params=parameters,
        )


class Extension(BaseModel):
    """Class represents an extension as a collection of actions."""

    name: str
    """Extension name. Unique name within a server"""

    description: Optional[str]
    """Description of extension scope and overview of its actions."""

    authors: str
    """Authors of the extension."""

    actions: List[ExtensionAction]

    def __init__(self, name: str, description: Optional[str],
                 authors: str, actions: List[ExtensionActionData],
                 client: AqueductClient):
        super().__init__(name=name, description=description,
                         authors=authors, actions=[])
        for action in actions:
            self.actions.append(ExtensionAction(self, action, client))
