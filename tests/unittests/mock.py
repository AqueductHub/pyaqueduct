from uuid import uuid4

from pyaqueduct.schemas.mutations import (
    add_tags_to_experiment_mutation,
    create_experiment_mutation,
    execute_extension_action_mutation,
    remove_tag_from_experiment_mutation,
    update_experiment_mutation,
)
from pyaqueduct.schemas.queries import (
    get_all_extensions_query,
    get_all_tags_query,
    get_experiment_query,
    get_experiments_query,
)


def patched_execute(self, query, variable_values, **kwargs):
    if query == create_experiment_mutation:
        return {
            "createExperiment": {
                "uuid": f"{uuid4()}",
                "title": variable_values["title"],
                "description": variable_values["description"],
                "eid": "230101-01",
                "tags": variable_values["tags"],
                "files": [],
                "createdAt": "2024-01-03T18:03:46.135824",
                "updatedAt": "2024-01-03T18:03:46.135829",
            }
        }

    elif query == update_experiment_mutation:
        return {
            "updateExperiment": {
                "uuid": variable_values["uuid"],
                "title": variable_values["title"],
                "description": variable_values["description"],
                "eid": "230101-01",
                "tags": [],
                "files": [],
                "createdAt": "2024-01-03T18:03:46.135824",
                "updatedAt": "2024-01-03T18:03:46.135829",
            }
        }

    elif query == get_experiment_query:
        return {
            "experiment": {
                "uuid": variable_values["value"],
                "title": "test title",
                "description": "test description",
                "eid": "230101-01",
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
                        "uuid": f"{uuid4()}",
                        "title": f"test title {idx}",
                        "description": f"test description {idx}",
                        "eid": f"230101-0{idx}",
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

    elif query == add_tags_to_experiment_mutation:
        return {
            "addTagsToExperiment": {
                "uuid": variable_values["uuid"],
                "title": "test title",
                "description": "test description",
                "eid": "230101-01",
                "tags": variable_values["tags"],
                "files": [],
                "createdAt": "2024-01-03T18:03:46.135824",
                "updatedAt": "2024-01-03T18:03:46.135829",
            }
        }

    elif query == remove_tag_from_experiment_mutation:
        return {
            "removeTagFromExperiment": {
                "uuid": variable_values["uuid"],
                "title": "test title",
                "description": "test description",
                "eid": "230101-01",
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

    elif query == get_all_extensions_query:
        return {
            "extensions": [
                {
                    "name": "Dummy extension",
                    "authors": "aqueduct@riverlane.com",
                    "description": "This extension prints environment variables passed to it. No requests to Aqueduct sent.\n",
                    "actions": [
                        {
                            "name": "echo",
                            "description": "Print values to stdout",
                            "experimentVariableName": "var4",
                            "parameters": [
                                {
                                    "name": "var1",
                                    "displayName": None,
                                    "description": "variable 1",
                                    "dataType": "str",
                                    "defaultValue": "1",
                                    "options": None,
                                },
                                {
                                    "name": "var2",
                                    "displayName": "some display name",
                                    "description": "variable 2",
                                    "dataType": "int",
                                    "defaultValue": None,
                                    "options": None,
                                },
                                {
                                    "name": "var3",
                                    "displayName": None,
                                    "description": "variable 3",
                                    "dataType": "float",
                                    "defaultValue": None,
                                    "options": None,
                                },
                                {
                                    "name": "var4",
                                    "displayName": None,
                                    "description": "variable 4",
                                    "dataType": "experiment",
                                    "defaultValue": None,
                                    "options": None,
                                },
                                {
                                    "name": "var5",
                                    "displayName": None,
                                    "description": "variable 5 multiline",
                                    "dataType": "textarea",
                                    "defaultValue": None,
                                    "options": None,
                                },
                                {
                                    "name": "var6",
                                    "displayName": None,
                                    "description": "boolean variable",
                                    "dataType": "bool",
                                    "defaultValue": "1",
                                    "options": None,
                                },
                                {
                                    "name": "var7",
                                    "displayName": None,
                                    "description": "select / combobox",
                                    "dataType": "select",
                                    "defaultValue": "string three",
                                    "options": ["string1", "string2", "string three", "string4"],
                                },
                            ],
                        },
                        {
                            "name": "echo_stderr",
                            "description": "Print values to stdout",
                            "experimentVariableName": "var4",
                            "parameters": [
                                {
                                    "name": "var1",
                                    "displayName": None,
                                    "description": "variable 1",
                                    "dataType": "str",
                                    "defaultValue": "1",
                                    "options": None,
                                },
                                {
                                    "name": "var2",
                                    "displayName": "some display name",
                                    "description": "variable 2",
                                    "dataType": "int",
                                    "defaultValue": None,
                                    "options": None,
                                },
                                {
                                    "name": "var3",
                                    "displayName": None,
                                    "description": "variable 3",
                                    "dataType": "float",
                                    "defaultValue": None,
                                    "options": None,
                                },
                                {
                                    "name": "var4",
                                    "displayName": None,
                                    "description": "variable 4",
                                    "dataType": "experiment",
                                    "defaultValue": None,
                                    "options": None,
                                },
                                {
                                    "name": "var5",
                                    "displayName": None,
                                    "description": "variable 5 multiline",
                                    "dataType": "textarea",
                                    "defaultValue": None,
                                    "options": None,
                                },
                                {
                                    "name": "var6",
                                    "displayName": None,
                                    "description": "boolean variable",
                                    "dataType": "bool",
                                    "defaultValue": "1",
                                    "options": None,
                                },
                                {
                                    "name": "var7",
                                    "displayName": None,
                                    "description": "select / combobox",
                                    "dataType": "select",
                                    "defaultValue": "string three",
                                    "options": ["string1", "string2", "string three", "string4"],
                                },
                            ],
                        },
                    ],
                },
            ]
        }

    elif query == execute_extension_action_mutation:
        return {
            "executeExtension": {
                "logExperiment": "234-4",
                "logFile": "Dummy extension-echo-20240510-135611.log",
                "returnCode": 0,
                "stderr": "",
                "stdout": (
                    "var1=a\nvar2=1\nvar3=1.0e-4\nvar4=234-4\n"
                    "var5=text\ntext\nvar6=0\nvar7=string1\n"
                    "dummykey=dummyvalue\n"
                ),
            }
        }
