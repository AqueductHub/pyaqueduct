# pylint: skip-file


from tempfile import NamedTemporaryFile

from pyaqueduct.api import API


def check_experiments(experiment, expected_experiment):
    assert expected_experiment.eid == experiment.eid
    assert expected_experiment.title == experiment.title
    assert expected_experiment.description == experiment.description
    assert expected_experiment.files == experiment.files
    assert expected_experiment.uuid == experiment.uuid
    assert expected_experiment.created_at == experiment.created_at
    assert expected_experiment.updated_at == experiment.updated_at


def test_connection():
    expected_title = "test title"
    expected_description = "test description"

    api = API(url="host.docker.internal:8000", timeout=1)

    api.create_experiment(title=expected_title, description=expected_description)


# def test_experiment_flow():
#     expected_title = "test title"
#     expected_description = "test description"

#     api = API(url="http://aqueductcore:8000", timeout=1)

#     experiment = api.create_experiment(title=expected_title, description=expected_description)

#     assert experiment.title == expected_title
#     assert experiment.description == expected_description

#     experiment_new = api.get_experiment_by_eid(eid=experiment.eid)

#     check_experiments(experiment, experiment_new)

#     experiment_new = api.get_experiment_by_uuid(uuid=experiment.uuid)

#     check_experiments(experiment, experiment_new)

#     with NamedTemporaryFile() as file1, NamedTemporaryFile() as file2, NamedTemporaryFile() as file3, NamedTemporaryFile() as file4:
#         experiment.upload_file(file1.name)
#         experiment.upload_file(file2.name)
#         experiment.upload_file(file3.name)
#         experiment.upload_file(file4.name)

#         experiment.remove_files(files=[file1.name.split("/")[-1], file2.name.split("/")[-1]])
#         assert sorted([item[0] for item in experiment.files]) == sorted(
#             [file3.name.split("/")[-1], file4.name.split("/")[-1]]
#         )


# def test_remove_experiment_by_eid():
#     expected_title = "test title"
#     expected_description = "test description"

#     api = API(url="http://aqueductcore:8000", timeout=1)

#     experiment = api.create_experiment(title=expected_title, description=expected_description)

#     api.remove_experiment_by_eid(eid=experiment.eid)


# def test_find_experiments():
#     expected_title = "test title"
#     expected_description = "test description"

#     experiments_list = []

#     api = API(url="http://aqueductcore:8000", timeout=1)

#     for _ in range(3):
#         experiment = api.create_experiment(title=expected_title, description=expected_description)
#         experiments_list.append(experiment)

#     experiments = api.find_experiments(search=expected_title, limit=10)

#     # reverse them list to match the order returned by the server (order by creation date)
#     experiments_list.reverse()

#     for experiment, expected_exp in zip(experiments, experiments_list):
#         check_experiments(experiment, expected_exp)
