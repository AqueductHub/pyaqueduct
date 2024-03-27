from uuid import uuid4

from pyaqueduct.schemas.mutations import (
    add_tag_to_experiment_mutation,
    create_experiment_mutation,
    remove_tag_from_experiment_mutation,
    update_experiment_mutation,
)
from pyaqueduct.schemas.queries import (
    get_all_tags_query,
    get_experiment_query,
    get_experiments_query,
)


def patched_execute(self, query, variable_values, **kwargs):
    if query == create_experiment_mutation:
        return {
            "createExperiment": {
                "id": f"{uuid4()}",
                "title": variable_values["title"],
                "description": variable_values["description"],
                "alias": "230101-01",
                "tags": variable_values["tags"],
                "files": [],
                "createdAt": "2024-01-03T18:03:46.135824",
                "updatedAt": "2024-01-03T18:03:46.135829",
            }
        }

    elif query == update_experiment_mutation:
        return {
            "updateExperiment": {
                "id": variable_values["experimentId"],
                "title": variable_values["title"],
                "description": variable_values["description"],
                "alias": "230101-01",
                "tags": [],
                "files": [],
                "createdAt": "2024-01-03T18:03:46.135824",
                "updatedAt": "2024-01-03T18:03:46.135829",
            }
        }

    elif query == get_experiment_query:
        return {
            "experiment": {
                "id": variable_values["value"],
                "title": "test title",
                "description": "test description",
                "alias": "230101-01",
                "tags": [],
                "createdAt": "2023-01-01T00:00:00",
                "updatedAt": "2023-01-01T00:00:00",
                "files": [],
            }
        }

    elif query == get_experiments_query:
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
                    for idx in range(1, variable_values["limit"] + 1)
                ],
                "totalExperimentsCount": variable_values["limit"],
            }
        }

    elif query == add_tag_to_experiment_mutation:
        return {
            "addTagToExperiment": {
                "id": variable_values["experimentId"],
                "title": "test title",
                "description": "test description",
                "alias": "230101-01",
                "tags": variable_values["tag"],
                "files": [],
                "createdAt": "2024-01-03T18:03:46.135824",
                "updatedAt": "2024-01-03T18:03:46.135829",
            }
        }

    elif query == remove_tag_from_experiment_mutation:
        return {
            "removeTagFromExperiment": {
                "id": variable_values["experimentId"],
                "title": "test title",
                "description": "test description",
                "alias": "230101-01",
                "tags": [],
                "files": [],
                "createdAt": "2024-01-03T18:03:46.135824",
                "updatedAt": "2024-01-03T18:03:46.135829",
            }
        }

    elif query == get_all_tags_query:
        return {
            "tags": {
                "tagsData": [f"tag_{idx}" for idx in range(1, variable_values["limit"] + 1)],
                "totalTagsCount": 15,
            }
        }
