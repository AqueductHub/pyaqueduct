import tempfile
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from uuid import uuid4

from gql.client import SyncClientSession
from httpx import Response

from pyaqueduct.client import AqueductClient
from tests.unittests.mock import patched_execute


def test_create_experiment(monkeypatch):
    expected_title = "test title"
    expected_description = "test description"
    expected_tags = []

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiment = client.create_experiment(
        title=expected_title, description=expected_description, tags=expected_tags
    )
    assert experiment.title == expected_title
    assert experiment.description == expected_description
    assert experiment.tags == expected_tags


def test_update_experiment(monkeypatch):
    experiment_uuid = uuid4()
    expected_title = "test title"
    expected_description = "test description"
    expected_tags = []

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiment = client.update_experiment(
        experiment_uuid=experiment_uuid, title=expected_title, description=expected_description
    )
    assert experiment.title == expected_title
    assert experiment.description == expected_description
    assert experiment.tags == expected_tags


def test_get_experiment(monkeypatch):
    experiment_id = uuid4()

    expected_title = "test title"
    expected_description = "test description"
    expected_tags = []

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiment = client.get_experiment(experiment_id)
    assert experiment.title == expected_title
    assert experiment.description == expected_description
    assert experiment.tags == expected_tags


def test_get_experiments(monkeypatch):
    expected_number_of_experiments = 7

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiments = client.get_experiments(limit=7, offset=0)
    assert len(experiments.experiments) == expected_number_of_experiments

    assert experiments.experiments[0].title == "test title 1"
    assert experiments.experiments[0].description == "test description 1"

    assert experiments.experiments[1].title == "test title 2"
    assert experiments.experiments[1].description == "test description 2"


def test_get_experiments_with_filters(monkeypatch):
    expected_number_of_experiments = 7

    start_datetime = datetime.now()
    end_datetime = start_datetime + timedelta(hours=1)
    tags = ["tag1", "tag2"]

    title = "search text"

    def patched_execute(self, query, variable_values, **kwargs):
        if variable_values["title"]:
            assert variable_values["title"] == title
        if variable_values["startDate"]:
            assert variable_values["startDate"] == start_datetime.isoformat()
        if variable_values["endDate"]:
            assert variable_values["endDate"] == end_datetime.isoformat()
        if variable_values["tags"]:
            assert variable_values["tags"] == tags
        return {
            "experiments": {
                "experimentsData": [
                    {
                        "id": f"{uuid4()}",
                        "title": f"test title {idx}",
                        "description": f"test description {idx}",
                        "alias": f"230101-0{idx}",
                        "tags": [],
                        "createdAt": "2023-01-01T00:00:00",
                        "updatedAt": "2023-01-01T00:00:00",
                        "files": [],
                    }
                    for idx in range(1, expected_number_of_experiments + 1)
                ],
                "totalExperimentsCount": expected_number_of_experiments,
            }
        }

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiments = client.get_experiments(
        title=title, limit=10, offset=10, start_datetime=start_datetime, end_datetime=end_datetime
    )
    assert len(experiments.experiments) == expected_number_of_experiments

    assert experiments.experiments[0].title == "test title 1"
    assert experiments.experiments[0].description == "test description 1"

    assert experiments.experiments[1].title == "test title 2"
    assert experiments.experiments[1].description == "test description 2"


def test_add_tags_to_experiment(monkeypatch):
    experiment_id = uuid4()

    expected_tags = ["tag1", "tag2"]
    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiment = client.add_tags_to_experiment(experiment_uuid=experiment_id, tags=expected_tags)

    assert expected_tags == experiment.tags


def test_remove_experiment(monkeypatch):
    experiment_id = uuid4()

    def patched_execute(self, query, variable_values, **kwargs):
        if variable_values["experimentId"]:
            assert variable_values["experimentId"] == str(experiment_id)

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    client.remove_experiment(experiment_uuid=experiment_id)


def test_remove_tag_from_experiment(monkeypatch):
    experiment_id = uuid4()
    tag_name = "tag"

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiment = client.remove_tag_from_experiment(experiment_uuid=experiment_id, tag=tag_name)

    assert tag_name not in experiment.tags


def test_get_tags(monkeypatch):
    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    tags = client.get_tags(limit=10, offset=0)

    assert len(tags.tags) == 10


def test_get_plugins(monkeypatch):
    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)
    client = AqueductClient(url="http://test.com", timeout=1)
    plugins = client.get_plugins()
    assert len(plugins) == 1
    assert len(plugins[0].functions) == 2
    assert plugins[0].functions[0].parameters[-1].dataType == "select"
    assert plugins[0].functions[0].parameters[-1].options[1] == "string2"


def test_execute_plugin_function(monkeypatch):
    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)
    client = AqueductClient(url="http://test.com", timeout=1)
    exec_result = client.execute_plugin_function(
        plugin="Dummy plugin",
        function="echo",
        params={
            "var1": "a",
            "var2": 1,
            "var3": False,
        }
    )
    assert exec_result.returnCode == 0
    assert exec_result.stdout != ""
    assert exec_result.stderr == ""


@patch("pyaqueduct.client.client.post")
def test_file_upload(fake_httpx_post):
    fake_httpx_post.return_value = Response(status_code=200)

    client = AqueductClient(url="http://test.com", timeout=1)

    with tempfile.NamedTemporaryFile() as file:
        data = client.upload_file(uuid4(), file.name)


@patch("pyaqueduct.client.client.stream")
def test_file_download(fake_httpx_stream, mocker):
    fake_httpx_stream.return_value.__enter__.return_value = mocker.Mock()
    fake_httpx_stream.return_value.__enter__.return_value.status_code = 200
    expected_content = [b"test response"]

    def iterable():
        bytes_downloaded = 0
        fake_httpx_stream.return_value.__enter__.return_value.num_bytes_downloaded = (
            bytes_downloaded
        )
        for item in expected_content:
            bytes_downloaded += 1
            yield item

    fake_httpx_stream.return_value.__enter__.return_value.iter_bytes.return_value = iterable()
    fake_httpx_stream.return_value.__enter__.return_value.num_bytes_downloaded = 0
    fake_httpx_stream.return_value.__enter__.return_value.headers = {
        "Content-Length": f"{str(len(expected_content))}"
    }

    client = AqueductClient(url="http://test.com", timeout=1)

    with tempfile.TemporaryDirectory() as dir:
        response = client.download_file(uuid4(), "sample.txt", dir)
