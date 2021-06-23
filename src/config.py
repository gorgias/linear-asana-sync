import os

from src.constants import Teams, AsanaCustomFieldLabels

ASANA_PERSONAL_TOKEN = os.environ["ASANA_PERSONAL_TOKEN"]
ASANA_WORKSPACE_ID = "488965188402817"
ASANA_ENGINEERING_TEAMS = {
    Teams.AUTOMATIONS: "982375050031828",
    Teams.CORE: "1200192869973721",
    Teams.DATA: "1200192869973737",
    Teams.DEVELOPER_RELATIONS: "1200192869973741",
    Teams.INTEGRATIONS: "1200192869973709",
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
ASANA_CUSTOM_FIELD_TEAM_ENUM_VALUES = {
    Teams.AUTOMATIONS: "1200210900372008",
    Teams.CORE: "1200210900372020",
    Teams.DATA: "1200210900372025",
    Teams.DEVELOPER_RELATIONS: "1200210900372031",
    Teams.INTEGRATIONS: "1200210900372036",
    Teams.SELF_SERVE: "1200210900372048",
    Teams.SRE: "1200210900372044",
}

LINEAR_PERSONAL_TOKEN = os.environ["LINEAR_PERSONAL_TOKEN"]
LINEAR_ENGINEERING_TEAMS = {
    "376f0c36-7c27-4d16-b9da-4f4c987cbe36": Teams.AUTOMATIONS,
    "e2d7941a-2a89-4290-8add-fbf54fe0721d": Teams.CORE,
    "4297897f-2700-4f80-89a2-0ba55ae1bde1": Teams.DATA,
    "6dc91a72-1cbb-4744-96f1-8c96aff1f91b": Teams.DEVELOPER_RELATIONS,
    "6a2c9cfe-e4b8-4adc-b7b5-8cbcf65e0d19": Teams.INTEGRATIONS,
    "0af154c0-beaf-4cda-abf2-5323d0f9ccac": Teams.SRE,
    "5d5a6d61-bad9-45c1-84ad-b360c020e5bf": Teams.SELF_SERVE,
}
LINEAR_MILESTONE_ASANA_PORTFOLIO = {"Q2 2021": "1200029345398157", "Q3 2021": "1200319317571240"}
