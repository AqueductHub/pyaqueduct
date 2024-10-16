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
        $taskId: UUID!,
    ) {
        task (
            taskId: $taskId
        ) {
            uuid
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
                files {
                    modifiedAt
                    name
                    path
                }
            }
            parameters {
                key {
                    dataType
                    defaultValue
                    description
                    displayName
                    options
                    name
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
        $actionName: String = null,
        $username: String = null,
        $startDate: DateTime = null,
        $endDate: DateTime = null,
    ) {
        tasks (
            offset: $offset,
            limit: $limit,
            filters: {
                extensionName: $extensionName,
                actionName: $actionName,
                username: $username,
                startDate: $startDate,
                endDate: $endDate,
            }
        ) {
            tasksData {
                uuid
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
                    files {
                        modifiedAt
                        name
                        path
                    }
                }
                parameters {
                    key {
                        dataType
                        defaultValue
                        description
                        displayName
                        options
                        name
                    }
                    value
                }
            }
            totalTasksCount
        }
    }
    """
)
