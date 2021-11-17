import os

from src.constants import Teams, AsanaCustomFieldLabels

ASANA_PERSONAL_TOKEN = os.environ["ASANA_PERSONAL_TOKEN"]
ASANA_WORKSPACE_ID = "488965188402817"
ASANA_TEAMS = {
    Teams.APPS_CHANNELS: "1201378198737247",
    Teams.APPS_DEVELOPER_RELATIONS: "1200192869973741",
    Teams.APPS_ECOMMERCE: "1201378198737254",
    Teams.AUTOMATIONS: "982375050031828",
    Teams.CORE: "1200192869973721",
    Teams.DATA: "1200192869973737",
    Teams.PRODUCT: "868907021768517",
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
    Teams.PRODUCT: "1197631589607089",
    Teams.SELF_SERVE: "1200210900372048",
    Teams.SRE: "1200210900372044",
}

LINEAR_PERSONAL_TOKEN = os.environ["LINEAR_PERSONAL_TOKEN"]
# To update the list run: flask info linear-team-ids
LINEAR_TEAMS = {
    "d9ed0e21-018e-4262-b997-a5975ff41840": Teams.APPS_CHANNELS,
    "6dc91a72-1cbb-4744-96f1-8c96aff1f91b": Teams.APPS_DEVELOPER_RELATIONS,
    "f7aa21ad-5da3-4c53-b7e8-929103befcbb": Teams.APPS_ECOMMERCE,
    "376f0c36-7c27-4d16-b9da-4f4c987cbe36": Teams.AUTOMATIONS,
    "e2d7941a-2a89-4290-8add-fbf54fe0721d": Teams.CORE,
    "4297897f-2700-4f80-89a2-0ba55ae1bde1": Teams.DATA,
    "feb53aee-0832-4ffb-8be6-1fad9014b6e1": Teams.PRODUCT,
    "5d5a6d61-bad9-45c1-84ad-b360c020e5bf": Teams.SELF_SERVE,
    "0af154c0-beaf-4cda-abf2-5323d0f9ccac": Teams.SRE,
}
LINEAR_MILESTONE_ASANA_PORTFOLIO = {"Q4 2021": "1200577199350401"}
