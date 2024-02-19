"""Aqueduct GraphQL Query schemas"""
from gql import gql

get_experiments_query = gql(
    """
    query GetExperiments (
        $limit: Int!,
        $offset: Int!,
        $title: String = "",
        $startDate: Date = null,
        $endDate: Date = null,
    ) {
        experiments (
            filters: {
                title: $title,
                startDate: $startDate,
                endDate: $endDate,
            }
            limit: $limit,
            offset: $offset,
        ) {
            experimentsData {
                id
                title
                description
                alias
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
        id
        title
        description
        alias
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
