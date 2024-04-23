"""Aqueduct application programming interface (API) module."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, HttpUrl, PositiveFloat, PrivateAttr

from pyaqueduct.client import AqueductClient
from pyaqueduct.experiment import _MAX_DESCRIPTION_LENGTH, _MAX_TITLE_LENGTH, Experiment
from pyaqueduct.settings import Settings


class API(BaseModel):
    """Aqueduct API interface to interact with experiments.

    Args:
        url: URL of the Aqueduct server including the prefix.
        timeout: Timeout of operations in seconds.

    """

    url: HttpUrl
    timeout: PositiveFloat

    _client: AqueductClient = PrivateAttr()

    def __init__(self, url: str, timeout: float = 0.5):
        super().__init__(url=url, timeout=timeout)

        if not url.endswith("/"):
            url = url + "/"
        api_url = f"{url}api"

        self._client = AqueductClient(url=api_url, timeout=timeout, api_token=Settings().api_token)

    def create_experiment(
        self,
        title: str = Field(..., min_length=1, max_length=_MAX_TITLE_LENGTH),
        description: str = Field("", max_length=_MAX_DESCRIPTION_LENGTH),
    ) -> Experiment:
        """Create an experiment with specific title and description.

        Args:
            title: Title of the experiment.
            description: Description of the experiment.

        Returns:
            Experiment object to interact with its data.

        """

        experiment_data = self._client.create_experiment(title=title, description=description)
        return Experiment(
            client=self._client,
            experiment_id=experiment_data.id,
            alias=experiment_data.alias,
            created_at=experiment_data.created_at,
        )

    def get_experiment(self, alias: str) -> Experiment:
        """Get the experiment by the specified identifier to operate on.

        Args:
            alias: Alias of the specified experiment.

        Returns:
            Experiment object to interact with the experiment data.

        """
        experiment_data = self._client.get_experiment_by_alias(alias=alias)
        return Experiment(
            client=self._client,
            experiment_id=experiment_data.id,
            alias=experiment_data.alias,
            created_at=experiment_data.created_at,
        )

    def find_experiments(self, search: str, limit: int, offset: int = 0) -> List[Experiment]:
        """Find the experiments that have the search criteria in their title or id.

        Args:
            search: The string to search for in the title field of experiments.
            limit: The maximum number of experiments to fetch in a single request.
            offset: The number of experiments to skip from the beginning of the search results.

        Returns:
            List of experiment objects to operate on their data.

        """
        experiments = self._client.get_experiments(
            title=search, limit=limit, offset=offset
        ).experiments
        return [
            Experiment(
                client=self._client,
                experiment_id=experiment.id,
                alias=experiment.alias,
                created_at=experiment.created_at,
            )
            for experiment in experiments
        ]
