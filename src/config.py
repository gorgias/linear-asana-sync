import os

from src.constants import AsanaCustomFieldLabels, Teams, Tribes

ASANA_PERSONAL_TOKEN = os.environ["ASANA_PERSONAL_TOKEN"]
ASANA_WORKSPACE_ID = "488965188402817"

ASANA_MASTER_PORTFOLIO = "1201614681408069"  # contains all the quarterly OKR/milestones

# https://app.asana.com/0/portfolio/1201150734315686/list
# Improve support performance to 2.8
# Modify milestone name and portfolio gid after creating it with flask create milestone-portfolio
LINEAR_MILESTONE_ASANA_PORTFOLIO = {"Q2 2022": "1201986191862785", "Q1 2022": "1201150734315686"}


ASANA_PORTFOLIO_TEMPLATE_ID = "1201479875410449"

# To add any members to the portfolio, add them here and run flask info update-milestone-portfolio-members Q2 2022
ASANA_PORTFOLIO_USERS_IDS = [
    "1200243002194193",  # Engineering Bot
    "1183822033025111",  # Thomas Trinelle
    "1197818354683322",  # Felix Enescu
    "1201660769578072",  # Paul Teyssier,
    "1201375948074808",  # Anas El Mhamdi
]

# To update the list run: flask info asana-team-ids
ASANA_TEAMS = {
    Teams.PLT_CORE: "1200192869973721",
    Teams.PLT_DEV_EXP: "1201626672125908",  # 1201626672125908: PE: Platform
    Teams.PLT_DATA: "1200192869973737",
    Teams.PLT_SERVICES: "1201626672538486",
    Teams.PLT_SRE: "1166955907061953",
    Teams.APP_CHANNELS: "1201378198737247",
    Teams.APP_DEVREL_ECOM: "1200192869973741",  # 1200192869973741: PE: Apps Developer Relations
    Teams.AUT_ADOPTION: "1201626672538490",  # 1201626672538490: PE: Automations
    Teams.AUT_PRODUCTIVITY: "982375050031828",
    Teams.AUT_SELF_SERVE: "1200192869973731",
}

ASANA_TASKS_CUSTOM_FIELDS = {
    AsanaCustomFieldLabels.LINEAR_URL: "1200210833927136",
}

ASANA_PROJECTS_CUSTOM_FIELDS = {
    AsanaCustomFieldLabels.LINEAR_URL: "1200210833927136",
    AsanaCustomFieldLabels.TEAM: "1118518032371299",
}

ASANA_PORTFOLIO_CUSTOM_FIELDS = {
    "milestone": {
        AsanaCustomFieldLabels.VALUE: "1168694676619590",
        AsanaCustomFieldLabels.GOAL: "1168700089398681",
        AsanaCustomFieldLabels.TEAM: "1118518032371299",
    },
    "tribe": {
        AsanaCustomFieldLabels.TEAM: "1118518032371299",
    },
    "squad": {
        AsanaCustomFieldLabels.LINEAR_URL: "1200210833927136",
        AsanaCustomFieldLabels.TEAM: "1118518032371299",
    },
}

# To update the list run: flask info asana-custom-team-ids
ASANA_CUSTOM_FIELD_TEAM = {
    Teams.PLT_CORE: "1200210900372020",
    Teams.PLT_DEV_EXP: "1201625293756972",
    Teams.PLT_DATA: "1200210900372025",
    Teams.PLT_SERVICES: "1201625293756971",
    Teams.PLT_SRE: "1200210900372044",
    Teams.APP_CHANNELS: "1201378227647192",
    Teams.APP_DEVREL_ECOM: "1201378227648256",
    Teams.AUT_ADOPTION: "1201623696888812",
    Teams.AUT_PRODUCTIVITY: "1200210900372008",
    Teams.AUT_SELF_SERVE: "1200210900372048",
}

ASANA_TRIBES_TEAMS_MAPPING = {
    Tribes.PLATFORM: [Teams.PLT_CORE, Teams.PLT_DEV_EXP, Teams.PLT_DATA, Teams.PLT_SERVICES, Teams.PLT_SRE],
    Tribes.APP: [Teams.APP_CHANNELS, Teams.APP_DEVREL_ECOM],
    Tribes.AUTOMATIONS: [Teams.AUT_ADOPTION, Teams.AUT_PRODUCTIVITY, Teams.AUT_SELF_SERVE],
}

LINEAR_PERSONAL_TOKEN = os.environ["LINEAR_PERSONAL_TOKEN"]

# To update the list run: flask info linear-team-ids
LINEAR_TEAMS = {
    "e2d7941a-2a89-4290-8add-fbf54fe0721d": Teams.PLT_CORE,
    "703bd385-8541-46e3-8ae4-c6df4ef55363": Teams.PLT_DEV_EXP,
    "4297897f-2700-4f80-89a2-0ba55ae1bde1": Teams.PLT_DATA,
    "1f36537b-7218-4dee-93bb-440ffe1ed3b2": Teams.PLT_SERVICES,
    "0af154c0-beaf-4cda-abf2-5323d0f9ccac": Teams.PLT_SRE,
    "d9ed0e21-018e-4262-b997-a5975ff41840": Teams.APP_CHANNELS,
    "0d0ff18f-650a-4c7f-8cd7-af779c91fe50": Teams.APP_DEVREL_ECOM,
    "bd9bff46-c93a-40d3-8b89-7dbc25a94211": Teams.AUT_ADOPTION,
    "376f0c36-7c27-4d16-b9da-4f4c987cbe36": Teams.AUT_PRODUCTIVITY,
    "5d5a6d61-bad9-45c1-84ad-b360c020e5bf": Teams.AUT_SELF_SERVE,
}

ASANA_TRIBES_PORTFOLIOS = {
    Tribes.PLATFORM: "1201623587508275",
    Tribes.APP: "1201623587670750",
    Tribes.AUTOMATIONS: "1201623716555278",
}

ASANA_TEAMS_PORTFOLIOS = {
    Tribes.PLATFORM: {
        Teams.PLT_CORE: "1201623743216304",
        Teams.PLT_DATA: "1201623813331521",
        Teams.PLT_DEV_EXP: "1201625452953632",
        Teams.PLT_SERVICES: "1201625378714104",
        Teams.PLT_SRE: "1201625103707973",
    },
    Tribes.APP: {
        Teams.APP_CHANNELS: "1201623774631001",
        Teams.APP_DEVREL_ECOM: "1201623775083302",
    },
    Tribes.AUTOMATIONS: {
        Teams.AUT_ADOPTION: "1201625138623587",
        Teams.AUT_PRODUCTIVITY: "1201624076028214",
        Teams.AUT_SELF_SERVE: "1201624076503388",
    },
}

ASANA_PROJECT_COLOR_RGB_MAP = {
    "dark-blue": [69, 115, 210],
    "dark-brown": [248, 223, 114],
    "dark-green": [93, 162, 131],
    "dark-orange": [212, 127, 101],
    "dark-pink": [217, 100, 160],
    "dark-purple": [127, 119, 208],
    "dark-red": [216, 96, 95],
    "dark-teal": [142, 207, 204],
    "dark-warm-gray": [98, 99, 100],
    "light-blue": [62, 103, 189],
    "light-green": [156, 186, 76],
    "light-orange": [216, 170, 97],
    "light-pink": [224, 153, 215],
    "light-purple": [161, 95, 190],
    "light-red": [226, 136, 138],
    "light-teal": [70, 182, 176],
    "light-warm-gray": [98, 99, 100],
    "light-yellow": [223, 200, 101],
}

LINEAR_ICONS_TO_ASANA = {
    "Project": "board",
    "Clock": "timeline",
    "Compass": "map",
    "Calendar": "calendar",
    "Page": "list",
    "Robot": "Computer",
    "Chat": "chat_bubbles",
    "LightBulb": "light_bulb",
    "Computer": "computer",
    "Megaphone": "megaphone",
    "Basket": "shopping_basket",
    "Briefcase": "briefcase",
    "Bank": "coins",
    "Dollar": "coins",
    "Euro": "coins",
    "Bitcoin": "coins",
    "Etherum": "coins",
    "Cart": "shopping_basket",
    "Shop": "shopping_basket",
    "Rocket": "rocket",
    "Mountain": "mountain_flag",
    "Bug": "bug",
    "Users": "people",
}
