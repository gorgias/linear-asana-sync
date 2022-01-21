from enum import Enum, unique

LINEAR_GRAPHQL_ENDPOINT = "https://api.linear.app/graphql"


@unique
class Teams(str, Enum):
    PLT_CORE = "[PLT-Core]"
    PLT_DEV_EXP = "[PLT Developer Experience]"
    PLT_DATA = "[PLT-Data]"
    PLT_SERVICES = "[PLT Services]"
    PLT_SRE = "[PLT-SRE]"

    APP_CHANNELS = "[APP-Channels]"
    APP_DEVREL_ECOM = "[APP DevRel + Ecom]"

    AUT_ADOPTION = "[AUT-Adoption]"
    AUT_PRODUCTIVITY = "[AUT-Productivity]"
    AUT_SELF_SERVE = "[AUT-Self Service]"


@unique
class Tribes(str, Enum):
    APP = "[APP]"
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
