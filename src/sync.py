import re

from flask import current_app

from src.asana_client import AsanaClient
from src.constants import AsanaCustomFieldLabels
from src.linear_client import LinearClient


def old_sync_asana_projects(milestone_name: str):
    """Create Asana projects from Linear projects"""

    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    asana_portfolio_gid = current_app.config["LINEAR_MILESTONE_ASANA_PORTFOLIO"][milestone_name]

    linear_client = LinearClient()
    linear_milestones = linear_client.milestones()
    linear_milestone_id = next(filter(lambda m: m["name"] == milestone_name, linear_milestones))["id"]
    linear_projects = linear_client.projects_by_milestone(linear_milestone_id)
    asana_projects_by_linear_url = asana_client.projects_in_portfolio_by_custom_field(
        asana_portfolio_gid,
        custom_field_gid=current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][AsanaCustomFieldLabels.LINEAR_URL],
    )

    for linear_project in linear_projects:
        existing_asana_project = None
        for (
            linear_project_url,
            asana_project_item,
        ) in asana_projects_by_linear_url.items():
            if linear_project["slugId"] in linear_project_url:
                existing_asana_project = asana_project_item
                break

        if not existing_asana_project:
            existing_asana_project = asana_client.create_project(linear_project, milestone_name)

        asana_client.update_project(existing_asana_project, linear_project)


def sync_asana_projects(milestone_name: str):
    """Create Asana projects from Linear projects"""
    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    asana_master_portfolio_gid = current_app.config["ASANA_MASTER_PORTFOLIO"]  # contains all quarterly portfolios
    asana_milestone_portfolio_gid = current_app.config["LINEAR_MILESTONE_ASANA_PORTFOLIO"][milestone_name]

    linear_client = LinearClient()
    linear_projects = []
    linear_projects = get_linear_projects(linear_client, milestone_name)

    for tribe, teams in current_app.config["ASANA_TEAMS_PORTFOLIOS"].items():
        current_app.logger.info(f"Sync tribe {tribe}")
        for team_name, team_portfolio_gid in teams.items():
            current_app.logger.info(f"Sync team {team_name}, portfoio id {team_portfolio_gid}")
            sync_team_portfolio(asana_client, linear_projects, team_name, team_portfolio_gid)


def sync_asana_projects_by_template(milestone_name: str):
    """Create Asana projects from Linear projects using a template"""
    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    asana_master_portfolio_gid = current_app.config["ASANA_MASTER_PORTFOLIO"]  # contains all quarterly portfolios
    asana_milestone_portfolio_gid = current_app.config["LINEAR_MILESTONE_ASANA_PORTFOLIO"][milestone_name]

    linear_client = LinearClient()

    # Get template portfolio and duplicate it
    asana_template_portfolio = asana_client.client.portfolios.get_portfolio(
        current_app.config["ASANA_PORTFOLIO_TEMPLATE_ID"]
    )
    asana_tribes_templates = list(
        asana_client.client.portfolios.get_items_for_portfolio(
            asana_template_portfolio["gid"], opt_fields=["name", "owner", "members"]
        )
    )
    asana_tribes_portfolios = asana_client.create_tribes_portfolios(
        asana_milestone_portfolio_gid, asana_tribes_templates
    )
    linear_projects = get_linear_projects(linear_client, milestone_name)
    handle_tribes_portfolios(asana_client, asana_tribes_portfolios, linear_projects)


def get_linear_projects(linear_client, milestone_name):
    current_app.logger.info(f"Fetching projects for milestone {milestone_name}")
    linear_milestones = linear_client.milestones()
    current_app.logger.debug(f"Milestones: {linear_milestones}")
    linear_milestone_id = next(filter(lambda m: m["name"] == milestone_name, linear_milestones))["id"]
    linear_projects = list(linear_client.projects_by_milestone(linear_milestone_id))
    current_app.logger.debug(f"Linear Projects: {linear_projects}")
    return linear_projects


def handle_tribes_portfolios(asana_client, asana_tribes_portfolios, linear_projects):
    for tribe_portfolio in asana_tribes_portfolios:
        current_app.logger.info(f"Handling tribe portfolio {tribe_portfolio['name']} - {tribe_portfolio['gid']}")
        tribe_portfolio_name = re.match("\[.*?\]", tribe_portfolio["name"]).group(0)
        tribe_portfolio_gid = tribe_portfolio["gid"]
        corresponding_squads = current_app.config["ASANA_TRIBES_TEAMS_MAPPING"].get(tribe_portfolio_name)

        if not corresponding_squads:
            current_app.logger.warning(f"No corresponding squads found for tribe portfolio {tribe_portfolio_name}")
            continue

        squads_portfolios = asana_client.create_squads_portfolios(tribe_portfolio_gid, corresponding_squads)
        handle_squad_portfolios(asana_client, linear_projects, squads_portfolios)


def sync_team_portfolio(asana_client, linear_projects, team_name, portfolio_gid):
    """Sync a squad/team protfolio"""
    current_app.logger.info(f"Syncing team portfolio {portfolio_gid}")
    portolio = asana_client.client.portfolios.get_portfolio(
        portfolio_gid, opt_fields=["gid", "name", "owner", "members", "custom_fields"]
    )
    portfolio_name = portolio["name"]

    current_app.logger.info(f"Syncing team {team_name} portfolio: {portfolio_name}")
    team_asana_projects = asana_client.projects_in_portfolio_by_custom_field(
        portfolio_gid,
        custom_field_gid=current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][AsanaCustomFieldLabels.LINEAR_URL],
    )
    current_app.logger.debug(
        "Projects in portfolio %s - %s by linear url %s: %s",
        portfolio_name,
        portfolio_gid,
        current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][AsanaCustomFieldLabels.LINEAR_URL],
        team_asana_projects,
    )

    team_linear_projects = [
        project for project in linear_projects if current_app.config["LINEAR_TEAMS"][project["team"]["id"]] == team_name
    ]
    current_app.logger.debug(
        "Linear projects for team %s: %s",
        team_name,
        team_linear_projects,
    )
    for team_linear_project in team_linear_projects:
        current_app.logger.info(
            f"Handling linear project {team_linear_project['name']} - {team_linear_project['slugId']}"
        )
        existing_asana_project = None
        for linear_project_url, asana_project_item in team_asana_projects.items():
            if team_linear_project["slugId"] in linear_project_url:
                existing_asana_project = asana_project_item
                break

        if not existing_asana_project:
            current_app.logger.info(f"Creating project {team_linear_project['name']}")
            existing_asana_project = asana_client.create_project(team_linear_project, portfolio_gid)
        else:
            current_app.logger.info(f"Project {existing_asana_project['name']} already exists")

        current_app.logger.info(f"Updating project {team_linear_project['name']}")
        asana_client.update_project(existing_asana_project, team_linear_project)


def handle_squad_portfolios(asana_client, linear_projects, squads_portfolios):
    for squad_portfolio in squads_portfolios:

        squad_portfolio_gid = squad_portfolio["gid"]
        squad_portfolio_name = squad_portfolio["name"]

        current_app.logger.info(f"Handling squad portfolio {squad_portfolio_name} - {squad_portfolio_gid}")

        asana_projects_by_linear_url = asana_client.projects_in_portfolio_by_custom_field(
            squad_portfolio_gid,
            custom_field_gid=current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][AsanaCustomFieldLabels.LINEAR_URL],
        )
        current_app.logger.debug(
            "Projects in portfolio %s - %s by linear url %s: %s",
            squad_portfolio_name,
            squad_portfolio_gid,
            current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][AsanaCustomFieldLabels.LINEAR_URL],
            asana_projects_by_linear_url,
        )

        squad_linear_projects = [
            project
            for project in linear_projects
            if squad_portfolio_name == current_app.config["LINEAR_TEAMS"][project["team"]["id"]]
        ]
        current_app.logger.debug(
            "Linear projects for squad %s: %s",
            squad_portfolio_name,
            squad_linear_projects,
        )

        for squad_linear_project in squad_linear_projects:
            current_app.logger.info(
                f"Handling linear project {squad_linear_project['name']} - {squad_linear_project['slugId']}"
            )
            existing_asana_project = None
            for (
                linear_project_url,
                asana_project_item,
            ) in asana_projects_by_linear_url.items():
                if squad_linear_project["slugId"] in linear_project_url:
                    existing_asana_project = asana_project_item

                    break

            if not existing_asana_project:
                current_app.logger.info(f"Creating project {squad_linear_project['name']}")
                existing_asana_project = asana_client.create_project(squad_linear_project, squad_portfolio_gid)
            else:
                current_app.logger.info(f"Project {existing_asana_project['name']} already exists")

            current_app.logger.info(f"Updating project {squad_linear_project['name']}")
            asana_client.update_project(existing_asana_project, squad_linear_project)


def create_milestone_portfolio(milestone_name: str):
    """Create Asana portfolio for milestone"""
    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    asana_master_portfolio_gid = current_app.config["ASANA_MASTER_PORTFOLIO"]

    asana_portfolio = {
        "name": milestone_name,
        "workspace": current_app.config["ASANA_WORKSPACE_ID"],
    }

    # Create the milestone portfolio (that contains tribes portfolios)
    current_app.logger.info(f"Creating milestone portfolio for milestone {milestone_name}")
    milestone_portfolio = asana_client.client.portfolios.create_portfolio(asana_portfolio)
    current_app.logger.debug(f"Created milestone portfolio %s", milestone_portfolio)

    # Add initial members to created portfolio
    new_members = {
        "members": current_app.config["ASANA_PORTFOLIO_USERS_IDS"],
    }
    current_app.logger.info(
        "Adding members to portfolio %s - %s: %s", milestone_portfolio["gid"], milestone_portfolio["name"], new_members
    )
    milestone_portfolio = asana_client.client.portfolios.add_members_for_portfolio(
        milestone_portfolio["gid"], new_members
    )

    # Add it to the master portfolio (the one that contains quarter's okrs)
    current_app.logger.info(f"Adding portfolio {milestone_portfolio['name']} to portfolio {asana_master_portfolio_gid}")
    body = {"item": f"{milestone_portfolio['gid']}"}
    asana_client.client.portfolios.add_item_for_portfolio(asana_master_portfolio_gid, body)

    return milestone_portfolio
