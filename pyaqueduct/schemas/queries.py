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
    query MyQuery {
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
