import datetime

import click
from flask import current_app
from flask.cli import AppGroup

from src.asana_client import AsanaClient
from src.constants import AsanaCustomFieldLabels
from src.linear_client import LinearClient
from src.sync import create_milestone_portfolio, sync_asana_projects

sync_commands = AppGroup("sync", help="Sync commands.")
create_commands = AppGroup("create", help="Create commands.")
info_commands = AppGroup("info", help="Fetching info commands.")


@sync_commands.command("asana-projects")
@click.argument("milestone_name", default="Q1 2022")
def asana_projects(milestone_name: str):
    """Create Asana projects from Linear projects"""
    start_time = datetime.datetime.now()
    sync_asana_projects(milestone_name)
    duration = datetime.datetime.now() - start_time
    current_app.logger.info(f"Finished syncing projects for milestone {milestone_name} in {duration}")


@create_commands.command("milestone-portfolio")
@click.argument("milestone_name", default="Q1 2022")
def milestone_portfolio(milestone_name: str):
    """Create milstone portfolio"""
    portfolio = create_milestone_portfolio(milestone_name)
    print(f"Created milestone portfolio {portfolio}")


@info_commands.command("asana-user-ids")
def asana_user_ids():
    """Fetch all Asana user ids"""
    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    for user in asana_client.users():
        print(f"{user['gid']}: {user['email']}")


@info_commands.command("asana-team-ids")
@click.argument("custom_field_id", default="")
def asana_team_ids(custom_field_id: str):
    """Fetch all values of the custom field"""
    if not custom_field_id:
        custom_field_id = current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][AsanaCustomFieldLabels.TEAM]

    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    response = asana_client.client.custom_fields.get_custom_field(custom_field_id)
    for options in response["enum_options"]:
        print(f"{options['gid']}: {options['name']}")


@info_commands.command("linear-team-ids")
def linear_team_ids():
    """Fetch linear team ids"""
    linear_client = LinearClient()
    teams = linear_client.teams()
    for team in teams["data"]["teams"]["nodes"]:
        print(f"{team['id']}: {team['name']}")
