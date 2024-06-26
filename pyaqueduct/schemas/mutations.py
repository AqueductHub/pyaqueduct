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

update_experiment_mutation = gql(
    """
    mutation UpdateExperiment(
        $uuid: UUID!,
        $title: String,
        $description: String
    ) {
        updateExperiment (
            uuid: $uuid,
            experimentUpdateInput: {
                title: $title,
                description: $description
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

add_tags_to_experiment_mutation = gql(
    """
    mutation AddTagToExperiment (
        $uuid: UUID!,
        $tags: [String!]!
    ) {
        addTagsToExperiment(
            experimentTagsInput: {
                uuid: $uuid,
                tags: $tags
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

remove_tag_from_experiment_mutation = gql(
    """
    mutation RemoveTagFromExperiment (
        $uuid: UUID!,
        $tag: String!
    ) {
        removeTagFromExperiment (
            experimentTagInput: {
                uuid: $uuid,
                tag: $tag
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

remove_experiment_mutation = gql(
    """
    mutation RemoveTagFromExperiment (
        $uuid: UUID!
        ) {
        removeExperiment(experimentRemoveInput: {uuid: $uuid})
    }
    """
)

execute_extension_action_mutation = gql(
    """
    mutation ExecuteExtension (
        $extension: String!,
        $action: String!,
        $params: [[String!]!]!,
    ) {
        executeExtension(
            params: $params,
            extension: $extension,
            action: $action,
        ) {
            logExperiment
            logFile
            returnCode
            stderr
            stdout
        }
    }
    """
)
