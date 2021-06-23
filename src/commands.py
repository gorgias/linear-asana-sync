import click
from flask.cli import AppGroup

from src.sync import sync_asana_projects

sync_commands = AppGroup("sync", help="Sync commands.")


@sync_commands.command("asana-projects")
@click.argument("milestone_name", default="Q3 2021")
def asana_projects(milestone_name: str):
    """Create Asana projects from Linear projects"""

    sync_asana_projects(milestone_name)
