import os

from src.constants import AsanaCustomFieldLabels, Teams, Tribes

ASANA_PERSONAL_TOKEN = os.environ["ASANA_PERSONAL_TOKEN"]
ASANA_WORKSPACE_ID = "488965188402817"

ASANA_MASTER_PORTFOLIO = "1201614681408069"  # contains all the quarterly OKR/milestones

# 1201619843525892 (old Felix one)
# https://app.asana.com/0/portfolio/1201150734315686/list
# Improve support performance to 2.8
LINEAR_MILESTONE_ASANA_PORTFOLIO = {"Q1 2022": "1201150734315686"}


ASANA_PORTFOLIO_TEMPLATE_ID = "1201479875410449"


ASANA_PORTFOLIO_USERS_IDS = [
    "1200243002194193",  # Engineering Bot
    "1183822033025111",  # Thomas Trinelle
    "1197818354683322",  # Felix Enescu
    "1201567624474026",  # Paul Teyssier
]


ASANA_TEAMS = {
    Teams.APPS_CHANNELS: "1201378198737247",
    Teams.APPS_DEVELOPER_RELATIONS: "1200192869973741",
    Teams.APPS_ECOMMERCE: "1201378198737254",
    Teams.AUTOMATIONS: "982375050031828",
    Teams.CORE: "1200192869973721",
    Teams.DATA: "1200192869973737",
    Teams.SRE: "1166955907061953",
    Teams.SELF_SERVE: "1200192869973731",
}

ASANA_TASKS_CUSTOM_FIELDS = {
    AsanaCustomFieldLabels.LINEAR_URL: "1200210833927136",
}

ASANA_PROJECTS_CUSTOM_FIELDS = {
    AsanaCustomFieldLabels.LINEAR_URL: "1200210833927136",
    AsanaCustomFieldLabels.TEAM: "1118518032371299",
}

# To update the list run: flask info asana-team-ids
ASANA_CUSTOM_FIELD_TEAM_ENUM_VALUES = {
    Teams.APPS_CHANNELS: "1201378227647192",
    Teams.APPS_DEVELOPER_RELATIONS: "1200210900372031",
    Teams.APPS_ECOMMERCE: "1201378227648256",
    Teams.AUTOMATIONS: "1200210900372008",
    Teams.CORE: "1200210900372020",
    Teams.DATA: "1200210900372025",
    Teams.SELF_SERVE: "1200210900372048",
    Teams.SRE: "1200210900372044",
}

ASANA_TRIBES_TEAMS_MAPPING = {
    Tribes.APPS: [Teams.APPS_CHANNELS, Teams.APPS_DEVELOPER_RELATIONS, Teams.APPS_ECOMMERCE],
    Tribes.PLATFORM: [Teams.CORE, Teams.DATA, Teams.SRE],
    Tribes.AUTOMATIONS: [Teams.SELF_SERVE, Teams.AUTOMATIONS],
}

LINEAR_PERSONAL_TOKEN = os.environ["LINEAR_PERSONAL_TOKEN"]

# To update the list run: flask info linear-team-ids
LINEAR_TEAMS = {
    "d9ed0e21-018e-4262-b997-a5975ff41840": Teams.APPS_CHANNELS,
    "6dc91a72-1cbb-4744-96f1-8c96aff1f91b": Teams.APPS_DEVELOPER_RELATIONS,
    "0d0ff18f-650a-4c7f-8cd7-af779c91fe50": Teams.APPS_ECOMMERCE,
    "376f0c36-7c27-4d16-b9da-4f4c987cbe36": Teams.AUTOMATIONS,
    "e2d7941a-2a89-4290-8add-fbf54fe0721d": Teams.CORE,
    "4297897f-2700-4f80-89a2-0ba55ae1bde1": Teams.DATA,
    "5d5a6d61-bad9-45c1-84ad-b360c020e5bf": Teams.SELF_SERVE,
    "0af154c0-beaf-4cda-abf2-5323d0f9ccac": Teams.SRE,
}
