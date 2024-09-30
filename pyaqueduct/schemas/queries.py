"""Aqueduct GraphQL Query schemas"""

from gql import gql

get_experiments_query = gql(
    """
    query GetExperiments (
        $limit: Int!,
        $offset: Int!,
        $title: String = null,
        $startDate: DateTime = null,
        $endDate: DateTime = null,
        $tags: [String!] = null
    ) {
        experiments (
            filters: {
                title: $title,
                startDate: $startDate,
                endDate: $endDate,
                tags: $tags
            }
            limit: $limit,
            offset: $offset,
        ) {
            experimentsData {
                uuid
                title
                description
                eid
                createdAt
                updatedAt
                tags
                files {
                    name
                    path
                    modifiedAt
                }
            }
            totalExperimentsCount
        }
    }
    """
)


get_experiment_query = gql(
    """
    query GetExperimentByIdentifier (
        $type: IDType!,
        $value: String!,
    ) {
      experiment (
        experimentIdentifier: {
            value: $value,
            type: $type,
        }
       ) {
        uuid
        title
        description
        eid
        createdAt
        updatedAt
        tags
        files {
            name
            path
            modifiedAt
        }
      }
    }
    """
)

get_all_tags_query = gql(
    """
    query GetAllTags (
        $limit: Int,
        $offset: Int,
        $dangling: Boolean
    ) {
    tags (
        limit: $limit,
        offset: $offset,
        filters: {
            includeDangling: $dangling
        }
    ) {
        tagsData
        totalTagsCount
    }
    }
    """
)


get_all_extensions_query = gql(
    """
    query GetAllExtensionsQuery {
        extensions {
            name, authors, description,
            actions {
                name, description, experimentVariableName,
                parameters {
                    name
                    displayName
                    description
                    dataType
                    defaultValue
                    options
                }
            }
        }
    }
    """
)


get_task_query = gql(
    """
    query GetTaskQuery (
        $taskId: String!,
    ) {
        task (
            taskId: $taskId
        ) {
            taskId
            taskStatus
            resultCode
            extensionName
            actionName
            createdBy
            receivedAt
            endedAt
            stdOut
            stdErr
            experiment {
                createdAt
                createdBy
                description
                eid
                tags
                title
                updatedAt
                uuid
            }
            parameters {
                key {
                    dataType
                    defaultValue
                    description
                    displayName
                    name
                    options
                }
                value
            }
        }
    }
    """
)


get_tasks_query = gql(
    """
    query GetTasksQuery (
        $limit: Int!,
        $offset: Int!,
        $extensionName: String = null,
        $experimentUuid: String = null,
        $actionName: String = null,
        $username: String = null,
        $startDate: DateTime = null,
        $endDate: DateTime = null,
    ) {
        tasks (
            filters: {
                experiment: {
                    type: UUID,
                    value: $experimentUuid
                },
                extensionName: $extensionName,
                actionName: $actionName,
                username: $username,
                startDate: $startDate,
                endDate: $endDate,
            },
            offset: $offset,
            limit: $limit,
        ) {
            tasksData {
                taskId
                extensionName
                actionName
                receivedAt
                createdBy
                endedAt
                resultCode
                stdErr
                stdOut
                taskStatus
                experiment {
                    uuid
                    title
                    description
                    createdAt
                    createdBy
                    eid
                    tags
                    updatedAt
                }
            }
            totalTasksCount
        }
    }
    """
)
