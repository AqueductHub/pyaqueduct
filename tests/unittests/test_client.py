import tempfile
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
    experiment_uuid = f"{uuid4()}"
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

    experiment = client.get_experiment(str(experiment_id))
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


def test_add_tag_to_experiment(monkeypatch):
    experiment_id = uuid4()
    tag_name = "tag"

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiment = client.add_tag_to_experiment(experiment_uuid=f"{experiment_id}", tag=tag_name)

    assert tag_name in experiment.tags


def test_remove_tag_from_experiment(monkeypatch):
    experiment_id = uuid4()
    tag_name = "tag"

    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    experiment = client.remove_tag_from_experiment(experiment_uuid=f"{experiment_id}", tag=tag_name)

    assert tag_name not in experiment.tags


def test_get_tags(monkeypatch):
    monkeypatch.setattr(SyncClientSession, "execute", patched_execute)

    client = AqueductClient(url="http://test.com", timeout=1)

    tags = client.get_tags(limit=10, offset=0)

    assert len(tags.tags) == 10


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
