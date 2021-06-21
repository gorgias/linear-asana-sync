from enum import unique, Enum

LINEAR_GRAPHQL_ENDPOINT = "https://api.linear.app/graphql"


@unique
class Teams(str, Enum):
    AUTOMATIONS = "Automations"
    CORE = "Core"
    DATA = "Data"
    DEVELOPER_RELATIONS = "Developer Relations"
    INTEGRATIONS = "Integrations"
    SRE = "SRE"
    SELF_SERVE = "Self-Serve"


@unique
class AsanaCustomFieldLabels(str, Enum):
    LINEAR_URL = "Linear URL"
    TEAM = "Team"


@unique
class AsanaResourceType(str, Enum):
    PROJECT = "project"
