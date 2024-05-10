# pylint: skip-file
from collections import namedtuple
from datetime import datetime
from uuid import uuid4

from gql.client import SyncClientSession
from tests.unittests.mock import patched_execute

from pyaqueduct.plugin import Plugin, PluginFunction, PluginParameter
from pyaqueduct.api import API
from pyaqueduct.client import AqueductClient, ExperimentData, ExperimentsInfo


def test_create_experiment(monkeypatch):
    expected_title = "test title"
    expected_description = "test description"

    expected_id = uuid4()
    expected_alias = "mock_alias"
    expected_datetime = datetime.now()

    def patched_create_experiment(self, title, description):
        assert title == expected_title
        assert description == expected_description
        return ExperimentData(
            id=expected_id,
            title=expected_title,
            description=expected_description,
            alias=expected_alias,
            created_at=expected_datetime,
            updated_at=expected_datetime,
        )

    monkeypatch.setattr(AqueductClient, "create_experiment", patched_create_experiment)
    api = API(url="http://test.com", timeout=1)

    experiment = api.create_experiment(title=expected_title, description=expected_description)

    assert experiment.alias == expected_alias
    assert experiment.id == expected_id
    assert experiment.created_at == expected_datetime


def test_get_experiment_by_alias(monkeypatch):
    expected_id = uuid4()
    expected_title = "test title"
    expected_description = "test description"
    expected_alias = "mock_alias"
    expected_datetime = datetime.now()

    def patched_get_experiment(self, alias):
        return ExperimentData(
            id=expected_id,
            title=expected_title,
            description=expected_description,
            alias=alias,
            created_at=expected_datetime,
            updated_at=expected_datetime,
        )

    monkeypatch.setattr(AqueductClient, "get_experiment_by_alias", patched_get_experiment)
    api = API(url="http://test.com", timeout=1)

    experiment = api.get_experiment(alias=expected_alias)

    assert experiment.alias == expected_alias
    assert experiment.id == expected_id
    assert experiment.created_at == expected_datetime


def test_find_experiments(monkeypatch):
    ExperimentMockData = namedtuple(
        "ExperimentData",
        "expected_id expected_title expected_description expected_alias expected_datetime",
    )
    experiments_list = []
    for _ in range(3):
        new_experiment = ExperimentMockData(
            uuid4(), "test title", "test description", "mock_alias", datetime.now()
        )
        experiments_list.append(new_experiment)

    def patched_get_experiments(self, title, limit, offset, tags, start_datetime, end_datetime):
        return ExperimentsInfo(
            experiments=[
                ExperimentData(
                    id=item.expected_id,
                    title=item.expected_title,
                    description=item.expected_description,
                    alias=item.expected_alias,
                    created_at=item.expected_datetime,
                    updated_at=item.expected_datetime,
                )
                for item in experiments_list
            ][offset:limit],
            total_count=limit,
        )

    monkeypatch.setattr(AqueductClient, "get_experiments", patched_get_experiments)
    api = API(url="http://test.com", timeout=1)

    experiments = api.find_experiments(search="test title", limit=3)

    for experiment, expected_exp in zip(experiments, experiments_list):
        assert experiment.alias == expected_exp.expected_alias
        assert experiment.id == expected_exp.expected_id
        assert experiment.created_at == expected_exp.expected_datetime


def test_get_plugins(monkeypatch):
    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)
    api = API(url="http://test.com", timeout=1)
    plugins = api.get_plugins()
    assert len(plugins) == 1
    assert isinstance(plugins[0], Plugin)
    assert len(plugins[0].functions) == 2
    assert isinstance(plugins[0].functions[0], PluginFunction)
    assert plugins[0].functions[0].parameters[-1].dataType == "select"
    assert plugins[0].functions[0].parameters[-1].options[1] == "string2"
    assert isinstance(plugins[0].functions[0].parameters[0], PluginParameter)
