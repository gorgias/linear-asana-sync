from typing import Optional, List, Dict

import asana
from asana.error import ForbiddenError
from flask import current_app

from src.constants import AsanaCustomFieldLabels, AsanaResourceType
from src.types import (
    LinearProject,
    AsanaUser,
    AsanaProject,
    AsanaTask,
    LinearIssue,
    AsanaCustomFields,
)


class AsanaClient:
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.client = asana.Client.access_token(
            current_app.config["ASANA_PERSONAL_TOKEN"]
        )
        self.asana_users = self.users()

    def users(self) -> List[AsanaUser]:
        current_app.logger.debug(f"fetching users")
        users = self.client.users.get_users(
            {"workspace": self.workspace_id}, opt_fields=["gid", "email"]
        )
        return list(users)

    def projects_in_portfolio_by_custom_field(
        self, portfolio_gid: str, custom_field_gid: str
    ) -> Dict[str, AsanaProject]:
        """Get all projects in portfolio with a Linear URL custom field"""

        projects = {}

        current_app.logger.debug(f"getting projects in portfolio {portfolio_gid}")
        items = self.client.portfolios.get_items_for_portfolio(
            portfolio_gid, opt_fields=["gid", "name", "resource_type", "custom_fields"]
        )

        for item in items:
            if item["resource_type"] != AsanaResourceType.PROJECT:
                continue

            for custom_field in item["custom_fields"]:
                if not (
                    custom_field["gid"] == custom_field_gid
                    and custom_field["text_value"]
                ):
                    continue

                projects[custom_field["text_value"]] = item
                break
        return projects

    def create_project(
        self, linear_project: LinearProject, milestone_name: str
    ) -> AsanaProject:
        """Create Asana project from linear project values"""

        linear_project_url = (
            f"https://linear.app/gorgias/project/{linear_project['slugId']}"
        )
        team_name = current_app.config["LINEAR_TEAMS"][
            linear_project["team"]["id"]
        ]

        asana_project = {
            "name": linear_project["name"],
            "notes": f"""Linear URL: {linear_project_url} 

{linear_project["description"]}""",
            "team": current_app.config["ASANA_TEAMS"][team_name],
        }

        current_app.logger.debug(f"creating project {asana_project['name']}")
        asana_project = self.client.projects.create_project(asana_project)

        # We can only add certain fields (ex: a custom field) to the project once it was added to the portfolio

        # add project to portfolio
        current_app.logger.debug(f"adding item to portfolio {milestone_name}")
        self.client.portfolios.add_item_for_portfolio(
            current_app.config["LINEAR_MILESTONE_ASANA_PORTFOLIO"][milestone_name],
            {"item": asana_project["gid"]},
        )

        # Add custom fields for the tasks in the project
        for custom_field_label, custom_field_id in current_app.config[
            "ASANA_TASKS_CUSTOM_FIELDS"
        ].items():
            current_app.logger.debug(
                f"adding custom field to project {custom_field_label}"
            )
            self.client.projects.add_custom_field_setting_for_project(
                asana_project["gid"], {"custom_field": custom_field_id}
            )

        asana_project_update = {
            "custom_fields": {
                current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][
                    AsanaCustomFieldLabels.LINEAR_URL
                ]: linear_project_url,
                # For some reason portfolios in Asana doesn't display the teams values on projects.
                # Instead we have to use a custom field for the team
                current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][
                    AsanaCustomFieldLabels.TEAM
                ]: current_app.config["ASANA_CUSTOM_FIELD_TEAM_ENUM_VALUES"][team_name],
            }
        }
        current_app.logger.debug(f"updating project {asana_project['name']}")
        self.client.projects.update_project(asana_project["gid"], asana_project_update)

        current_app.logger.info(f"Asana project created: {asana_project['name']}")

        # fetch the project again with the latest fields
        current_app.logger.debug(f"re-fetching project: {asana_project['name']}")
        return self.client.projects.get_project(asana_project["gid"])

    def update_project(
        self, asana_project: AsanaProject, linear_project: LinearProject
    ):

        asana_project_update: AsanaProject = {}  # noqa

        followers = set()
        for asana_user in self.asana_users:
            if (
                linear_project["lead"]
                and asana_user["email"] == linear_project["lead"]["email"]
            ):
                asana_project_update["owner"] = asana_user["gid"]
            if linear_project["members"]:
                for linear_project_member in linear_project["members"]["nodes"]:
                    if linear_project_member["email"] == asana_user["email"]:
                        followers.add(asana_user["gid"])
        if followers:
            current_app.logger.debug(
                f"adding followers to project {asana_project['name']}"
            )
            try:
                self.client.projects.add_followers_for_project(
                    asana_project["gid"], {"followers": ",".join(followers)}
                )
            except ForbiddenError:
                current_app.logger.error(f"Failed to add followers: {followers}")

        if linear_project["targetDate"]:
            asana_project_update["due_on"] = linear_project["targetDate"]

        current_app.logger.debug(f"updating project")
        self.client.projects.update_project(asana_project["gid"], asana_project_update)

        current_app.logger.info(f"Asana project updated: {asana_project['name']}")

        self.sync_tasks(linear_project, asana_project["gid"])

    def _create_task(
        self, asana_project_gid: str, linear_issue: LinearIssue
    ) -> AsanaTask:
        asana_task: AsanaTask = {  # noqa
            "assignee": None,
            "completed": False,
            "due_on": linear_issue["dueDate"],
            "name": linear_issue["title"],
            "notes": linear_issue["description"] or "",
            "projects": [asana_project_gid],
            "workspace": self.workspace_id,
        }
        current_app.logger.debug(f"creating task")
        return self.client.tasks.create_task(asana_task)

    def _update_task(
        self,
        existing_asana_task: AsanaTask,
        linear_issue: LinearIssue,
        custom_fields: AsanaCustomFields,
    ):
        asana_task: AsanaTask = {  # noqa
            "assignee": None,
            "completed": False,
            "custom_fields": custom_fields,
            "due_on": linear_issue["dueDate"],
            "name": linear_issue["title"],
            "notes": linear_issue["description"] or "",
        }

        # set task completion
        if (
            linear_issue["completedAt"]
            or linear_issue["canceledAt"]
            or linear_issue["archivedAt"]
        ):
            asana_task["completed"] = True

        # assignee and followers
        followers = set()
        # set asana assignee if we have one in Linear
        for asana_user in self.asana_users:
            if (
                linear_issue["assignee"]
                and asana_user["email"] == linear_issue["assignee"]["email"]
            ):
                asana_task["assignee"] = asana_user["gid"]
            if linear_issue["subscribers"]:
                for linear_user in linear_issue["subscribers"]["nodes"]:
                    if asana_user["email"] == linear_user["email"]:
                        followers.add(asana_user["gid"])

        current_app.logger.debug(f"updating task {existing_asana_task['gid']}")
        self.client.tasks.update_task(existing_asana_task["gid"], asana_task)

        # followers
        existing_followers = set(
            user["gid"] for user in existing_asana_task["followers"]  # noqa
        )
        if followers != existing_followers:  # we have a change in followers
            followers_to_add = followers - existing_followers
            followers_to_remove = existing_followers - followers

            if followers_to_add:
                self.client.tasks.add_followers_for_task(
                    existing_asana_task["gid"], {"followers": list(followers_to_add)}
                )
            if followers_to_remove:
                self.client.tasks.remove_follower_for_task(
                    existing_asana_task["gid"], {"followers": list(followers_to_remove)}
                )

    def sync_tasks(self, linear_project: LinearProject, asana_project_gid: str):
        """Sync Asana tasks with Linear issues."""

        linear_url_custom_field_gid = current_app.config[
            "ASANA_PROJECTS_CUSTOM_FIELDS"
        ][AsanaCustomFieldLabels.LINEAR_URL]

        asana_task_fields = ["gid", "followers", "custom_fields", "completed"]

        current_app.logger.debug(f"fetching project tasks {linear_project['name']}")
        existing_asana_tasks = self.client.tasks.get_tasks_for_project(
            asana_project_gid, opt_fields=asana_task_fields
        )
        existing_asana_tasks_by_linear_url = {}
        for existing_asana_task in existing_asana_tasks:
            for custom_field in existing_asana_task["custom_fields"]:
                if custom_field["gid"] == linear_url_custom_field_gid:
                    existing_asana_tasks_by_linear_url[
                        custom_field["text_value"]
                    ] = existing_asana_task

        for linear_issue in linear_project["issues"]["nodes"]:
            linear_url_custom_field_text_value = (
                f"https://linear.app/gorgias/issue/{linear_issue['identifier']}"
            )

            # linear issue was already synced since there is already an Asana task that has the linear issue attached
            existing_asana_task = existing_asana_tasks_by_linear_url.get(
                linear_url_custom_field_text_value
            )
            custom_fields = {
                linear_url_custom_field_gid: linear_url_custom_field_text_value
            }
            if not existing_asana_task:
                existing_asana_task = self._create_task(asana_project_gid, linear_issue)
                current_app.logger.info(
                    f"Asana task created: {linear_issue['identifier']}"
                )
            self._update_task(existing_asana_task, linear_issue, custom_fields)
