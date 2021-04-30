from flask import current_app

from src.asana_client import AsanaClient
from src.constants import AsanaCustomFieldLabels
from src.linear_client import LinearClient


def sync_asana_projects(milestone_name: str):
    """Create Asana projects from Linear projects"""

    asana_client = AsanaClient(current_app.config["ASANA_WORKSPACE_ID"])
    asana_portfolio_gid = current_app.config["LINEAR_MILESTONE_ASANA_PORTFOLIO"][
        milestone_name
    ]

    linear_client = LinearClient()
    linear_milestones = linear_client.milestones()
    linear_milestone_id = next(
        filter(lambda m: m["name"] == milestone_name, linear_milestones)
    )["id"]
    linear_projects = linear_client.projects_by_milestone(linear_milestone_id)
    asana_projects_by_linear_url = asana_client.projects_in_portfolio_by_custom_field(
        asana_portfolio_gid,
        custom_field_gid=current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][
            AsanaCustomFieldLabels.LINEAR_URL
        ],
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
            existing_asana_project = asana_client.create_project(
                linear_project, milestone_name
            )

        asana_client.update_project(existing_asana_project, linear_project)
