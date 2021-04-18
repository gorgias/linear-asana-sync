import click
from flask import current_app
from flask.cli import AppGroup

from src.asana_client import AsanaClient
from src.constants import AsanaCustomFieldLabels
from src.linear_client import LinearClient

sync_commands = AppGroup("sync", help="Sync commands.")


@sync_commands.command("asana-projects")
@click.argument("milestone_name", default="Q2 2021")
def sync_asana_projects(milestone_name: str):
    """Create Asana projects from Linear projects"""

    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    asana_portfolio_gid = current_app.config["LINEAR_MILESTONE_ASANA_PORTFOLIO"][milestone_name]

    linear_client = LinearClient()
    linear_milestones = linear_client.milestones()
    linear_milestone_id = next(
        filter(lambda m: m["name"] == milestone_name, linear_milestones)
    )["id"]
    linear_projects = linear_client.projects_by_milestone(linear_milestone_id)

    for linear_project in linear_projects:
        # only interested in eng teams - a project can have only 1 team anyway, not sure why linear has a list of teams
        linear_project["team"] = next(
            filter(
                lambda t: t["id"] in current_app.config["LINEAR_ENGINEERING_TEAMS"],
                linear_project["teams"]["nodes"],
            )
        )

        # search Asana for a project that has a linear project slugId in it's URL
        asana_project = asana_client.find_project_in_portfolio(
            asana_portfolio_gid,
            custom_field_gid=current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][
                AsanaCustomFieldLabels.LINEAR_URL
            ],
            custom_field_value=linear_project["slugId"],
        )

        if not asana_project:
            asana_project = asana_client.create_project(linear_project, milestone_name)

        asana_client.update_project(asana_project, linear_project)
