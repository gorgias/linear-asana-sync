import click
from flask import current_app
from flask.cli import AppGroup

from src.asana_client import AsanaClient
from src.constants import AsanaCustomFieldLabels
from src.linear_client import LinearClient
from src.sync import sync_asana_projects

sync_commands = AppGroup("sync", help="Sync commands.")
info_commands = AppGroup("info", help="Fetching info commands.")


@sync_commands.command("asana-projects")
@click.argument("milestone_name", default="Q4 2021")
def asana_projects(milestone_name: str):
    """Create Asana projects from Linear projects"""

    sync_asana_projects(milestone_name)


@info_commands.command("asana-team-ids")
@click.argument("custom_field_id", default="")
def asana_team_ids(custom_field_id: str):
    """Fetch all values of the custom field"""

    if not custom_field_id:
        custom_field_id = current_app.config['ASANA_PROJECTS_CUSTOM_FIELDS'][AsanaCustomFieldLabels.TEAM]

    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    response = asana_client.client.custom_fields.get_custom_field(custom_field_id)
    for options in response['enum_options']:
        print(f"{options['gid']}: {options['name']}")


@info_commands.command("linear-team-ids")
def linear_team_ids():
    """Fetch linear team ids"""

    linear_client = LinearClient()
    teams = linear_client.teams()
    for team in teams['data']['teams']['nodes']:
        print(f"{team['id']}: {team['name']}")
