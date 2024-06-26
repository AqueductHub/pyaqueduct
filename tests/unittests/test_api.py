# pylint: skip-file
from collections import namedtuple
from datetime import datetime
from uuid import uuid4

from gql.client import SyncClientSession
from tests.unittests.mock import patched_execute

from pyaqueduct.extensions import Extension, ExtensionAction
from pyaqueduct.api import API
from pyaqueduct.client import AqueductClient, ExperimentData, ExperimentsInfo


def test_create_experiment(monkeypatch):
    expected_title = "test title"
    expected_description = "test description"

    expected_uuid = uuid4()
    expected_eid = "mock_eid"
    expected_datetime = datetime.now()

    def patched_create_experiment(self, title, description):
        assert title == expected_title
        assert description == expected_description
        return ExperimentData(
            uuid=expected_uuid,
            title=expected_title,
            description=expected_description,
            eid=expected_eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
        )

    monkeypatch.setattr(AqueductClient, "create_experiment", patched_create_experiment)
    api = API(url="http://test.com", timeout=1)

    experiment = api.create_experiment(title=expected_title, description=expected_description)

    assert experiment.eid == expected_eid
    assert experiment.uuid == expected_uuid
    assert experiment.created_at == expected_datetime


def test_get_experiment_by_eid(monkeypatch):
    expected_uuid = uuid4()
    expected_title = "test title"
    expected_description = "test description"
    expected_eid = "mock_eid"
    expected_datetime = datetime.now()

    def patched_get_experiment(self, eid):
        return ExperimentData(
            uuid=expected_uuid,
            title=expected_title,
            description=expected_description,
            eid=eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
        )

    monkeypatch.setattr(AqueductClient, "get_experiment_by_eid", patched_get_experiment)
    api = API(url="http://test.com", timeout=1)

    experiment = api.get_experiment(eid=expected_eid)

    assert experiment.eid == expected_eid
    assert experiment.uuid == expected_uuid
    assert experiment.created_at == expected_datetime


def test_remove_experiment_by_eid(monkeypatch):
    expected_uuid = uuid4()
    expected_title = "test title"
    expected_description = "test description"
    expected_eid = "mock_eid"
    expected_datetime = datetime.now()

    def patched_remove_experiment(self, experiment_uuid):
        assert experiment_uuid == expected_uuid

    def patched_get_experiment(self, eid):
        assert eid == expected_eid

        return ExperimentData(
            uuid=expected_uuid,
            title=expected_title,
            description=expected_description,
            eid=eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
        )

    monkeypatch.setattr(AqueductClient, "get_experiment_by_eid", patched_get_experiment)
    monkeypatch.setattr(AqueductClient, "remove_experiment", patched_remove_experiment)
    api = API(url="http://test.com", timeout=1)

    api.remove_experiment_by_eid(eid=expected_eid)


def test_find_experiments(monkeypatch):
    ExperimentMockData = namedtuple(
        "ExperimentData",
        "expected_uuid expected_title expected_description expected_eid expected_datetime",
    )
    experiments_list = []
    for _ in range(3):
        new_experiment = ExperimentMockData(
            uuid4(), "test title", "test description", "mock_eid", datetime.now()
        )
        experiments_list.append(new_experiment)

    def patched_get_experiments(self, title, limit, offset, tags, start_datetime, end_datetime):
        return ExperimentsInfo(
            experiments=[
                ExperimentData(
                    uuid=item.expected_uuid,
                    title=item.expected_title,
                    description=item.expected_description,
                    eid=item.expected_eid,
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
        assert experiment.eid == expected_exp.expected_eid
        assert experiment.uuid == expected_exp.expected_uuid
        assert experiment.created_at == expected_exp.expected_datetime


def test_get_extensions(monkeypatch):
    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)
    api = API(url="http://test.com", timeout=1)
    extensions = api.get_extensions()
    assert len(extensions) == 1
    assert isinstance(extensions[0], Extension)
    assert len(extensions[0].actions) == 2
    assert isinstance(extensions[0].actions[0], ExtensionAction)
    assert extensions[0].actions[0].name == "echo"
    assert extensions[0].actions[0].description == "Print values to stdout"
    assert extensions[0].actions[0].experiment_variable_name == "var4"
    assert extensions[0].actions[0].parameters[-1].dataType == "select"
    assert extensions[0].actions[0].parameters[-1].options[1] == "string2"


def test_execute_extension_action(monkeypatch):
    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)
    api = API(url="http://test.com", timeout=1)
    extensions = api.get_extensions()
    result = extensions[0].actions[0].execute({"var1": 1})
    assert result.returnCode == 0
    assert result.stdout != ""
    assert result.stderr == ""
