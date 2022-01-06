from enum import Enum, unique

LINEAR_GRAPHQL_ENDPOINT = "https://api.linear.app/graphql"


@unique
class Teams(str, Enum):
    APPS_CHANNELS = "[APP-Channels]"
    APPS_DEVELOPER_RELATIONS = "[APP-DevRel]"
    APPS_ECOMMERCE = "[APP-Ecommerce]"
    AUTOMATIONS = "[AUT-Productivity]"
    SELF_SERVE = "[AUT-Self Service]"
    CORE = "[PLT-Core]"
    DATA = "[PLT-Data]"
    SRE = "[PLT-SRE & Security]"


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
