from typing import List, Generator

import requests
from flask import current_app

from src.constants import LINEAR_GRAPHQL_ENDPOINT
from src.types import LinearMilestone, LinearProject


class LinearClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": current_app.config["LINEAR_PERSONAL_TOKEN"]}
        )

    def engineering_teams(self):
        response = self.session.post(
            LINEAR_GRAPHQL_ENDPOINT, json={"query": "{teams{nodes{id name}}}"}
        )
        response.raise_for_status()
        return response.json()

    def milestones(self) -> List[LinearMilestone]:
        response = self.session.post(
            LINEAR_GRAPHQL_ENDPOINT, json={"query": "{milestones{nodes{id name}}}"}
        )
        response.raise_for_status()
        return response.json()["data"]["milestones"]["nodes"]

    def projects_by_milestone(self, milestone_id: str) -> Generator[LinearProject, None, None]:
        """Get all projects and top-level issues of a milestone"""

        response = self.session.post(
            LINEAR_GRAPHQL_ENDPOINT,
            json={
                "query": """
                {
                    milestone(id: "%s") {
                        projects{nodes{id}}
                    }
                }""" % milestone_id
            },
        )
        if not response.ok:
            print(response.content)
            response.raise_for_status()

        project_ids = [p['id'] for p in response.json()["data"]["milestone"]["projects"]["nodes"]]

        for project_id in project_ids:
            response = self.session.post(
                LINEAR_GRAPHQL_ENDPOINT,
                json={
                    "query": """{
project(id: "%s") {
  slugId
  name
  description
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
  issues {
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
}}""" % project_id
                },
            )
            if not response.ok:
                print(response.content)
                response.raise_for_status()

            yield response.json()['data']['project']
