from enum import unique, Enum

LINEAR_GRAPHQL_ENDPOINT = "https://api.linear.app/graphql"


@unique
class Teams(str, Enum):
    APPS_CHANNELS = "Apps: Channels"
    APPS_DEVELOPER_RELATIONS = "Apps: Developer Relations"
    APPS_ECOMMERCE = "Apps: Ecommerce"
    AUTOMATIONS = "Automations"
    CORE = "Core"
    DATA = "Data"
    PRODUCT = "Product"
    SELF_SERVE = "Self-Serve"
    SRE = "SRE"


@unique
class AsanaCustomFieldLabels(str, Enum):
    LINEAR_URL = "Linear URL"
    TEAM = "Team"


@unique
class AsanaResourceType(str, Enum):
    PROJECT = "project"
