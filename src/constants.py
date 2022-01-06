from enum import Enum, unique

LINEAR_GRAPHQL_ENDPOINT = "https://api.linear.app/graphql"


@unique
class Teams(str, Enum):
    CORE = "[PLT-Core]"
    DEV_EXP = "[PLT Developer Experience]"
    DATA = "[PLT-Data]"
    SERVICES = "[PLT Services]"
    SRE = "[PLT-SRE]"

    APPS_ECOMMERCE = "[APP-Ecommerce]"
    APPS_CHANNELS = "[APP-Channels]"
    APPS_DEVELOPER_RELATIONS = "[APP-DevRel]"

    AUTOMATIONS = "[AUT-Productivity]"
    ADOPTION = "[AUT-Adoption]"
    SELF_SERVE = "[AUT-Self Service]"


@unique
class Tribes(str, Enum):
    APPS = "[APP]"
    PLATFORM = "[PLT]"
    AUTOMATIONS = "[AUT]"


@unique
class AsanaCustomFieldLabels(str, Enum):
    LINEAR_URL = "Linear URL"
    TEAM = "Team"
    TRIBE = "Tribe"


@unique
class AsanaResourceType(str, Enum):
    PROJECT = "project"
    PORTFOLIO = "portfolio"
