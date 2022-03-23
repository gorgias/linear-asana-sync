import re
from queue import Queue
from typing import Dict, List, Optional

import asana
import numpy as np
from asana.error import ForbiddenError
from colour import Color
from flask import current_app

from src.constants import AsanaCustomFieldLabels, AsanaResourceType
from src.types import (
    AsanaCustomFields,
    AsanaPortfolio,
    AsanaProject,
    AsanaTask,
    AsanaTeam,
    AsanaUser,
    LinearIssue,
    LinearProject,
)


class AsanaClient:
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.client = asana.Client.access_token(current_app.config["ASANA_PERSONAL_TOKEN"])
        self.asana_users = self.users()

    def users(self) -> List[AsanaUser]:
        current_app.logger.debug(f"fetching users")
        users = self.client.users.get_users({"workspace": self.workspace_id}, opt_fields=["gid", "email"])
        return list(users)

    def teams(self) -> List[AsanaTeam]:
        current_app.logger.debug(f"fetching teams")
        teams = self.client.teams.get_teams_for_organization(self.workspace_id, opt_fields=["gid", "name"])
        return list(teams)

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
                if not (custom_field["gid"] == custom_field_gid and custom_field["text_value"]):
                    continue

                projects[custom_field["text_value"]] = item
                break
        return projects

    def create_tribes_portfolios(self, parent_portfolio: str, asana_tribes_templates) -> List[AsanaPortfolio]:
        current_app.logger.info(f"creating tribes portfolios from templates")
        current_app.logger.debug(f"items in asana_tribes_templates: {asana_tribes_templates}")
        current_app.logger.debug(f"parent portfolio id: {parent_portfolio}")

        items_in_parent_portfolio = list(self.client.portfolios.get_items_for_portfolio(parent_portfolio))
        current_app.logger.debug(f"items in parent portfolio: {items_in_parent_portfolio}")
        pattern = "\[.*?\]"

        tribes_name = {}
        for item in items_in_parent_portfolio:
            match = re.match(pattern, item["name"])
            if match:
                tribes_name[match.group(0)] = item

        current_app.logger.debug(f"tribes_name: {tribes_name}")

        asana_tribes_portfolios = []
        for tribe_template in asana_tribes_templates:
            # If portfolio already exists, then continue
            tribe_name = re.match(pattern, tribe_template["name"]).group(0)
            if tribe_name in tribes_name:
                current_app.logger.debug(f"{tribe_template['name']} already exists")
                asana_tribes_portfolios.append(tribes_name[tribe_name])
                continue

            new_portfolio_body = {
                "workspace": current_app.config["ASANA_WORKSPACE_ID"],
                "name": f"{tribe_template['name']}",
                "color": tribe_template["color"],
            }

            # Create a portfolio per tribe
            current_app.logger.info(f"Creating a portfolio for tribe: {tribe_template['name']}")
            asana_portfolio = self.client.portfolios.create_portfolio(new_portfolio_body)

            # Add initial members to created portfolio
            new_members = set(current_app.config["ASANA_PORTFOLIO_USERS_IDS"])
            new_members.add(tribe_template["owner"]["gid"])
            new_members.update(x["gid"] for x in tribe_template["members"])
            new_members_payload = {"members": list(new_members)}
            asana_portfolio = self.client.portfolios.add_members_for_portfolio(
                asana_portfolio["gid"], new_members_payload
            )

            asana_tribes_portfolios.append(asana_portfolio)

            # Add custom fields to the tribe portfolios
            custom_fields = current_app.config["ASANA_PORTFOLIO_CUSTOM_FIELDS"]["tribe"]
            self.add_custom_fields_to_portfolio(asana_portfolio["gid"], custom_fields)

            # Add it to the parent portfolio
            current_app.logger.info(f"Adding portfolio {asana_portfolio['name']} to portfolio {parent_portfolio}")
            body = {"item": f"{asana_portfolio['gid']}"}
            self.client.portfolios.add_item_for_portfolio(parent_portfolio, body)

        return asana_tribes_portfolios

    def create_squads_portfolios(self, parent_portfolio: str, squads) -> List[AsanaPortfolio]:
        current_app.logger.info(f"creating squads portfolios")
        items_in_parent_portfolio = list(
            self.client.portfolios.get_items_for_portfolio(parent_portfolio, opt_fields=["name", "owner", "members"])
        )
        current_app.logger.debug(f"items in parent portfolio: {items_in_parent_portfolio}")
        squads_name = [item["name"] for item in items_in_parent_portfolio]

        for squad in squads:
            if squad.value in squads_name:
                current_app.logger.debug(f"{squad.value} already exists")
                continue

            tribe_color = self.client.portfolios.get_portfolio(parent_portfolio, opt_fields=["color"])["color"]
            new_portfolio_body = {
                "workspace": current_app.config["ASANA_WORKSPACE_ID"],
                "name": f"{squad.value}",
                "color": tribe_color,
            }

            # Create a portfolio per squad
            current_app.logger.info(f"Creating a portfolio for squad: {squad.value}")
            asana_portfolio = self.client.portfolios.create_portfolio(new_portfolio_body)
            # Add initial members to created portfolio
            new_members = {
                "members": current_app.config["ASANA_PORTFOLIO_USERS_IDS"],
            }
            asana_portfolio = self.client.portfolios.add_members_for_portfolio(asana_portfolio["gid"], new_members)

            items_in_parent_portfolio.append(asana_portfolio)

            # Add it to the tribe portfolio
            current_app.logger.info(f"Adding portfolio {asana_portfolio['name']} to portfolio {parent_portfolio}")
            body = {"item": f"{asana_portfolio['gid']}"}
            self.client.portfolios.add_item_for_portfolio(parent_portfolio, body)

            # Add custom fields on squad portfolios
            custom_fields = current_app.config["ASANA_PORTFOLIO_CUSTOM_FIELDS"]["squad"]
            self.add_custom_fields_to_portfolio(asana_portfolio["gid"], custom_fields)

        return items_in_parent_portfolio

    def create_project(self, linear_project: LinearProject, squad_portfolio_gid: str) -> AsanaProject:
        """Create Asana project from linear project values"""

        linear_project_url = f"https://linear.app/gorgias/project/{linear_project['slugId']}"
        team_name = current_app.config["LINEAR_TEAMS"][linear_project["team"]["id"]]

        asana_project = {
            "name": linear_project["name"],
            "notes": f"Linear URL: {linear_project_url}\n{linear_project['description']}",
            "team": current_app.config["ASANA_TEAMS"][team_name],
            "color": self._closest_asana_color(linear_project["color"]),
        }
        if current_app.config["LINEAR_ICONS_TO_ASANA"].get(linear_project["icon"]):
            asana_project["icon"] = current_app.config["LINEAR_ICONS_TO_ASANA"][linear_project["icon"]]

        current_app.logger.debug(f"creating project {asana_project['name']}")
        asana_project = self.client.projects.create_project(asana_project)

        # We can only add certain fields (ex: a custom field) to the project once it was added to the portfolio

        # add project to portfolio
        current_app.logger.debug(f"adding item to portfolio {squad_portfolio_gid}")
        self.client.portfolios.add_item_for_portfolio(
            squad_portfolio_gid,
            {"item": asana_project["gid"]},
        )

        # Add custom fields for the project
        for custom_field_label, custom_field_id in current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"].items():
            current_app.logger.debug(f"adding custom field to project {custom_field_label}")
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
                current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][AsanaCustomFieldLabels.TEAM]: current_app.config[
                    "ASANA_CUSTOM_FIELD_TEAM"
                ][team_name],
            }
        }
        current_app.logger.debug(f"updating project {asana_project['name']}")
        self.client.projects.update_project(asana_project["gid"], asana_project_update)

        # Add initial members to created project
        new_members = {
            "members": current_app.config["ASANA_PORTFOLIO_USERS_IDS"],
        }
        asana_project = self.client.projects.add_members_for_project(asana_project["gid"], new_members)

        current_app.logger.info(f"Asana project created: {asana_project['name']}")

        # fetch the project again with the latest fields
        current_app.logger.debug(f"re-fetching project: {asana_project['name']}")
        asana_project = self.client.projects.get_project(asana_project["gid"])
        current_app.logger.debug(f"project fetched: {asana_project}")
        return asana_project

    def update_project(self, asana_project: AsanaProject, linear_project: LinearProject):

        asana_project_update: AsanaProject = {}  # noqa
        asana_project_update["name"] = linear_project["name"]
        asana_project_update["color"] = self._closest_asana_color(linear_project["color"])
        if current_app.config["LINEAR_ICONS_TO_ASANA"].get(linear_project["icon"]):
            asana_project_update["icon"] = current_app.config["LINEAR_ICONS_TO_ASANA"][linear_project["icon"]]

        followers = set()
        for asana_user in self.asana_users:
            if linear_project["lead"] and asana_user["email"] == linear_project["lead"]["email"]:
                asana_project_update["owner"] = asana_user["gid"]
            if linear_project["members"]:
                for linear_project_member in linear_project["members"]["nodes"]:
                    if linear_project_member["email"] == asana_user["email"]:
                        followers.add(asana_user["gid"])
        if followers:
            current_app.logger.debug(f"adding followers to project {asana_project['name']}")
            try:
                self.client.projects.add_followers_for_project(asana_project["gid"], {"followers": ",".join(followers)})
            except ForbiddenError:
                current_app.logger.error(f"Failed to add followers: {followers}")

        if linear_project["targetDate"]:
            asana_project_update["due_on"] = linear_project["targetDate"]

        current_app.logger.debug(f"updating project {asana_project['name']}: {asana_project_update}")
        self.client.projects.update_project(asana_project["gid"], asana_project_update)

        current_app.logger.info(f"Asana project updated: {asana_project['name']}")

        self.sync_tasks(linear_project, asana_project["gid"])

    def sync_tasks(self, linear_project: LinearProject, asana_project_gid: str):
        """Sync Asana tasks with Linear issues."""
        current_app.logger.info(
            f"Syncing tasks for project {asana_project_gid}, linear project {linear_project['slugId']}"
        )

        linear_url_custom_field_gid = current_app.config["ASANA_PROJECTS_CUSTOM_FIELDS"][
            AsanaCustomFieldLabels.LINEAR_URL
        ]

        asana_task_fields = ["gid", "followers", "custom_fields", "completed"]

        current_app.logger.debug(f"fetching project tasks {linear_project['name']}")
        existing_asana_tasks = self.client.tasks.get_tasks_for_project(asana_project_gid, opt_fields=asana_task_fields)
        existing_asana_tasks_by_linear_url = {}
        for existing_asana_task in existing_asana_tasks:
            for custom_field in existing_asana_task["custom_fields"]:
                if custom_field["gid"] == linear_url_custom_field_gid:
                    existing_asana_tasks_by_linear_url[custom_field["text_value"]] = existing_asana_task
        current_app.logger.debug(f"existing tasks: {existing_asana_tasks_by_linear_url}")

        for linear_issue in linear_project["issues"]["nodes"]:
            linear_url_custom_field_text_value = f"https://linear.app/gorgias/issue/{linear_issue['identifier']}"
            current_app.logger.debug(f"sync task for linear issue {linear_issue['identifier']}")

            # linear issue was already synced since there is already an Asana task that has the linear issue attached
            existing_asana_task = existing_asana_tasks_by_linear_url.get(linear_url_custom_field_text_value)
            custom_fields = {linear_url_custom_field_gid: linear_url_custom_field_text_value}
            if not existing_asana_task:
                current_app.logger.debug(f"creating task for linear issue {linear_issue['identifier']}")
                existing_asana_task = self._create_task(asana_project_gid, linear_issue)
                current_app.logger.info(f"Asana task created: {linear_issue['identifier']}")
            else:
                current_app.logger.debug(f"task already exists for linear issue {linear_issue['identifier']}")

            self._update_task(existing_asana_task, linear_issue, custom_fields)

    def delete_all_portfolio_items(self, portfolio_id: str):
        q = Queue()
        all_portfolio_items = self._get_portfolio_items(portfolio_id)
        # store portfolios in queue
        for item in all_portfolio_items:
            if item["resource_type"] == "portfolio":
                q.put(item)
        # get nested portfolios and projects
        while not q.empty():
            portfolio = q.get()
            portfolio_items = self._get_portfolio_items(portfolio["gid"])
            all_portfolio_items.extend(portfolio_items)
            for item in portfolio_items:
                if item["resource_type"] == "portfolio":
                    q.put(item)
        # delete everything
        for item in all_portfolio_items:
            if item["resource_type"] == "portfolio":
                self._delete_portfolio(item["gid"])
            if item["resource_type"] == "project":
                self._delete_project(item["gid"])
        # # finally delete the empty shell
        # self._delete_portfolio(portfolio_id)
        return

    def add_custom_fields_to_portfolio(self, portfolio_id: str, custom_fields: dict):
        # Add custom fields on portfolios
        for custom_field_label, custom_field_id in custom_fields.items():
            current_app.logger.info(f"adding custom field {custom_field_label} to portfolio")
            self.client.portfolios.add_custom_field_setting_for_portfolio(
                portfolio_id, {"custom_field": custom_field_id}
            )
        return

    def _create_task(self, asana_project_gid: str, linear_issue: LinearIssue) -> AsanaTask:
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

    def _delete_portfolio(self, portfolio_id: str):
        return self.client.portfolios.delete_portfolio(portfolio_id)

    def _delete_project(self, project_id: str):
        return self.client.projects.delete_project(project_id)

    def _get_portfolio_items(self, portfolio_id: str):
        return list(self.client.portfolios.get_items_for_portfolio(portfolio_id))

    def _closest_asana_color(self, hexstring: str):
        asana_color_map = current_app.config["ASANA_PROJECT_COLOR_RGB_MAP"]
        colors = np.array(list(asana_color_map.values()))
        c = Color(hexstring)
        color = np.array(list(map(lambda x: round(x * 255), c.rgb)))
        distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))
        smallest_distance = colors[index_of_smallest][0]
        return next(c for c in asana_color_map if list(asana_color_map[c]) == list(smallest_distance))

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
        if linear_issue["completedAt"] or linear_issue["canceledAt"] or linear_issue["archivedAt"]:
            asana_task["completed"] = True

        # assignee and followers
        followers = set()
        # set asana assignee if we have one in Linear

        for asana_user in self.asana_users:
            if linear_issue["assignee"] and asana_user["email"] == linear_issue["assignee"]["email"]:
                asana_task["assignee"] = asana_user["gid"]
            if linear_issue["subscribers"]:
                for linear_user in linear_issue["subscribers"]["nodes"]:
                    if asana_user["email"] == linear_user["email"]:
                        followers.add(asana_user["gid"])

        current_app.logger.debug(f"updating task {linear_issue['identifier']} - {existing_asana_task['gid']}")
        self.client.tasks.update_task(existing_asana_task["gid"], asana_task)

        # followers
        existing_followers = set(user["gid"] for user in existing_asana_task["followers"])  # noqa
        # make sure the followers still exist
        asana_users = set(user["gid"] for user in self.asana_users)
        existing_followers.intersection_update(asana_users)

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
