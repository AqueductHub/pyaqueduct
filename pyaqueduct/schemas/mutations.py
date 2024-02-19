"""Aqueduct GraphQL Mutation schemas"""
from gql import gql

create_experiment_mutation = gql(
    """
    mutation CreateExperiment (
        $title: String!,
        $description: String!,
        $tags: [String!]!
    ) {
        createExperiment (
            createExperimentInput: {
                title: $title,
                description: $description,
                tags: $tags
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

update_experiment_mutation = gql(
    """
    mutation UpdateExperiment(
        $experimentId: UUID!,
        $title: String,
        $description: String
    ) {
        updateExperiment (
            experimentId: $experimentId,
            experimentUpdateInput: {
                title: $title,
                description: $description
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

add_tag_to_experiment_mutation = gql(
    """
    mutation AddTagToExperiment (
        $experimentId: UUID!,
        $tag: String!
    ) {
        addTagToExperiment (
            experimentTagInput: {
                experimentId: $experimentId,
                tag: $tag
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

remove_tag_from_experiment_mutation = gql(
    """
    mutation RemoveTagFromExperiment (
        $experimentId: UUID!,
        $tag: String!
    ) {
        removeTagFromExperiment (
            experimentTagInput: {
                experimentId: $experimentId,
                tag: $tag
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
