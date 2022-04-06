from enum import Enum, unique

LINEAR_GRAPHQL_ENDPOINT = "https://api.linear.app/graphql"


@unique
class Teams(str, Enum):
    PLT_CORE = "Core Platform:"
    PLT_DEV_EXP = "Dev Experience:"
    PLT_DATA = "Data Platform:"
    PLT_SERVICES = "Platform Services:"
    PLT_SRE = "SRE:"

    APP_CHANNELS = "Channels:"
    APP_DEVREL_ECOM = "Dev Relations & Ecommerce:"

    AUT_ADOPTION = "Help Center & Chat:"
    AUT_PRODUCTIVITY = "Productivity:"
    AUT_SELF_SERVE = "Self-Service:"
    AUT_CHAT = "Chat:"
    AUT_HELP_CENTER = "Help Center:"


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
    VALUE = "Value"
    GOAL = "Goal"


@unique
class AsanaResourceType(str, Enum):
    PROJECT = "project"
    PORTFOLIO = "portfolio"
