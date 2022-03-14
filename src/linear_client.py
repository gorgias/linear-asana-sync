from typing import Generator, List

import requests
from flask import current_app

from src.constants import LINEAR_GRAPHQL_ENDPOINT
from src.types import LinearMilestone, LinearProject


class LinearClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": current_app.config["LINEAR_PERSONAL_TOKEN"]})

    def teams(self):
        response = self.session.post(LINEAR_GRAPHQL_ENDPOINT, json={"query": "{teams{nodes{id name}}}"})
        response.raise_for_status()
        return response.json()

    def milestones(self) -> List[LinearMilestone]:
        current_app.logger.debug("fetching milestones")
        response = self.session.post(LINEAR_GRAPHQL_ENDPOINT, json={"query": "{milestones{nodes{id name}}}"})
        response.raise_for_status()
        return response.json()["data"]["milestones"]["nodes"]

    def projects_by_milestone(self, milestone_id: str) -> Generator[LinearProject, None, None]:
        """Get all projects and top-level issues of a milestone"""

        current_app.logger.debug("fetching milestone projects")
        response = self.session.post(
            LINEAR_GRAPHQL_ENDPOINT,
            json={
                "query": """
                {
                    milestone(id: "%s") {
                        projects(first: 150){nodes{id,url,teams{nodes{id}}}}
                    }
                }"""
                % milestone_id
            },
        )

        if not response.ok:
            current_app.logger.error(response.content)
            response.raise_for_status()

        linear_projects = {p["id"]: p for p in response.json()["data"]["milestone"]["projects"]["nodes"]}

        for project_id, project_props in linear_projects.items():
            # only fetch project details of teams that we're interested in
            team_ids = [
                t["id"] for t in project_props["teams"]["nodes"] if t["id"] in current_app.config["LINEAR_TEAMS"]
            ]
            if not team_ids:
                continue

            current_app.logger.debug(f"fetching project {project_props['url']}")
            response = self.session.post(
                LINEAR_GRAPHQL_ENDPOINT,
                json={
                    "query": """{
project(id: "%s") {
  slugId
  name
  description
  color
  state
  startDate
  startedAt
  targetDate
  completedAt
  completedIssueCountHistory
  completedScopeHistory
  issueCountHistory
  sortOrder
  lead {
    email
  }
  members {
    nodes {
      email
    }
  }
  teams {
    nodes {
      id
    }
  }
  issues(first:100) {
    nodes {
      identifier
      title
      priorityLabel
      description
      startedAt
      archivedAt
      canceledAt
      completedAt
      dueDate
      boardOrder
      assignee {
        email
      }
      subscribers {
        nodes {
          email
        }
      }
    }
  }
}}"""
                    % project_id
                },
            )
            if not response.ok:
                current_app.logger.error(response.content)
                response.raise_for_status()

            project = response.json()["data"]["project"]
            # only interested in some teams - a project can have only 1 team anyway
            project["team"] = next(
                filter(
                    lambda t: t["id"] in current_app.config["LINEAR_TEAMS"],
                    project["teams"]["nodes"],
                )
            )

            if project["team"]:
                yield project
