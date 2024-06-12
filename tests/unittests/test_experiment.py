# pylint: skip-file
from collections import namedtuple
from datetime import datetime
from uuid import uuid4

from pyaqueduct.client import AqueductClient, ExperimentData, ExperimentFile
from pyaqueduct.experiment import Experiment


def test_experiment_title(monkeypatch):
    expected_id = uuid4()
    expected_title = "test title"
    expected_description = "test description"
    expected_eid = "test_eid"
    expected_creation_datetime = datetime.now()
    expected_updated_datetime = datetime.now()

    def patched_get_experiment(self, experiment_uuid):
        return ExperimentData(
            uuid=experiment_uuid,
            title=expected_title,
            description=expected_description,
            eid=expected_eid,
            created_at=expected_creation_datetime,
            updated_at=expected_updated_datetime,
        )

    def patched_update_experiment(self, experiment_uuid, title):
        assert title == "new title"
        return ExperimentData(
            uuid=experiment_uuid,
            title=title,
            description=expected_description,
            eid=expected_eid,
            created_at=expected_creation_datetime,
            updated_at=expected_updated_datetime,
        )

    monkeypatch.setattr(AqueductClient, "get_experiment", patched_get_experiment)
    monkeypatch.setattr(AqueductClient, "update_experiment", patched_update_experiment)
    mocked_client = AqueductClient(url="http://test.com", timeout=1)
    experiment = Experiment(
        client=mocked_client,
        uuid=expected_id,
        eid=expected_eid,
        created_at=datetime.now(),
    )

    assert experiment.title == expected_title
    experiment.title = "new title"
    assert experiment.updated_at == expected_updated_datetime


def test_experiment_description(monkeypatch):
    expected_id = uuid4()
    expected_title = "test title"
    expected_description = "test description"
    expected_eid = "test_eid"
    expected_datetime = datetime.now()

    def patched_get_experiment(self, experiment_uuid):
        return ExperimentData(
            uuid=experiment_uuid,
            title=expected_title,
            description=expected_description,
            eid=expected_eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
        )

    def patched_update_experiment(self, experiment_uuid, description):
        assert description == "new description"
        return ExperimentData(
            uuid=experiment_uuid,
            title=expected_title,
            description=description,
            eid=expected_eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
        )

    monkeypatch.setattr(AqueductClient, "get_experiment", patched_get_experiment)
    monkeypatch.setattr(AqueductClient, "update_experiment", patched_update_experiment)
    mocked_client = AqueductClient(url="http://test.com", timeout=1)
    experiment = Experiment(
        client=mocked_client,
        uuid=expected_id,
        eid=expected_eid,
        created_at=datetime.now(),
    )

    assert experiment.description == expected_description
    experiment.description = "new description"


def test_experiment_tags(monkeypatch):
    expected_id = uuid4()
    expected_title = "test title"
    expected_description = "test description"
    expected_eid = "test_eid"
    expected_datetime = datetime.now()
    expected_tags = ["tag1", "tag2", "tag3"]

    def patched_get_experiment(self, experiment_uuid):
        return ExperimentData(
            uuid=experiment_uuid,
            title=expected_title,
            description=expected_description,
            eid=expected_eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
            tags=expected_tags,
        )

    def patched_add_tags_to_experiment(self, experiment_uuid, tags):
        assert tags == ["tag4", "tag5"]
        expected_tags.extend(tags)
        return ExperimentData(
            uuid=experiment_uuid,
            title=expected_title,
            description=expected_description,
            eid=expected_eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
            tags=expected_tags,
        )

    def patched_remove_tag_from_experiment(self, experiment_uuid, tag):
        assert tag == "tag4"
        expected_tags.remove(tag)
        return ExperimentData(
            uuid=experiment_uuid,
            title=expected_title,
            description=expected_description,
            eid=expected_eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
            tags=expected_tags,
        )

    monkeypatch.setattr(AqueductClient, "get_experiment", patched_get_experiment)
    monkeypatch.setattr(AqueductClient, "add_tags_to_experiment", patched_add_tags_to_experiment)
    monkeypatch.setattr(
        AqueductClient, "remove_tag_from_experiment", patched_remove_tag_from_experiment
    )
    mocked_client = AqueductClient(url="http://test.com", timeout=1)
    experiment = Experiment(
        client=mocked_client,
        uuid=expected_id,
        eid=expected_eid,
        created_at=datetime.now(),
    )

    assert experiment.tags == expected_tags
    experiment.add_tags(["tag4", "tag5"])
    assert expected_tags == ["tag1", "tag2", "tag3", "tag4", "tag5"]
    assert experiment.tags == expected_tags
    experiment.remove_tag("tag4")
    assert expected_tags == ["tag1", "tag2", "tag3", "tag5"]
    assert experiment.tags == expected_tags


def test_experiment_files(monkeypatch):
    expected_id = uuid4()
    expected_title = "test title"
    expected_description = "test description"
    expected_eid = "test_eid"
    expected_datetime = datetime.now()
    expected_tags = ["tag1", "tag2", "tag3"]
    expected_files = [ExperimentFile(name="file1", path="path1", modified_at=datetime.now())]

    def patched_get_experiment(self, experiment_uuid):
        return ExperimentData(
            uuid=experiment_uuid,
            title=expected_title,
            description=expected_description,
            eid=expected_eid,
            created_at=expected_datetime,
            updated_at=expected_datetime,
            tags=expected_tags,
            files=expected_files,
        )

    def patched_download_file(self, experiment_uuid, file_name, destination_dir):
        assert experiment_uuid == expected_id
        assert file_name == "new_file_path.json"
        assert destination_dir == "/tmp"

    def patched_upload_file(self, experiment_uuid, file):
        assert experiment_uuid == expected_id
        assert file == "/tmp/new_file_path.json"

    monkeypatch.setattr(AqueductClient, "get_experiment", patched_get_experiment)
    monkeypatch.setattr(AqueductClient, "download_file", patched_download_file)
    monkeypatch.setattr(AqueductClient, "upload_file", patched_upload_file)

    mocked_client = AqueductClient(url="http://test.com", timeout=1)
    experiment = Experiment(
        client=mocked_client,
        uuid=expected_id,
        eid=expected_eid,
        created_at=datetime.now(),
    )

    assert experiment.files == [(item.name, item.modified_at) for item in expected_files]
    experiment.upload_file(file="/tmp/new_file_path.json")
    experiment.download_file(file_name="new_file_path.json", destination_dir="/tmp")
