from typing import Dict, List, Optional, TypedDict


class LinearUser(TypedDict):
    id: str
    name: str
    email: str


class LinearUsers(TypedDict):
    nodes: List[LinearUser]


class LinearTeam(TypedDict):
    id: str
    name: str


class LinearTeams(TypedDict):
    nodes: List[LinearTeam]


class LinearSubscribers(TypedDict):
    nodes: List[LinearUser]


class LinearIssue(TypedDict):
    identifier: str
    title: str
    priorityLabel: str
    description: str
    startedAt: Optional[str]
    completedAt: Optional[str]
    canceledAt: Optional[str]
    archivedAt: Optional[str]
    dueDate: Optional[str]
    boardOrder: float
    assignee: LinearUser
    subscribers: LinearSubscribers


class LinearIssues(TypedDict):
    nodes: List[LinearIssue]


class LinearMilestone(TypedDict):
    id: str


class LinearProject(TypedDict):
    slugId: str
    name: str
    description: str
    icon: str
    color: str
    state: str

    startDate: Optional[str]
    startedAt: Optional[str]
    targetDate: Optional[str]
    completedAt: Optional[str]
    completedIssueCountHistory: List[int]
    completedScopeHistory: List[int]
    issueCountHistory: List[int]
    sortOrder: float

    lead: LinearUser
    members: LinearUsers
    teams: LinearTeams
    team: LinearTeam
    issues: LinearIssues


class AsanaUser(TypedDict):
    gid: str
    email: str


class AsanaTeam(TypedDict):
    gid: str
    name: str


AsanaCustomFields = Dict[str, str]


class AsanaTask(TypedDict):
    gid: Optional[str]
    assignee: Optional[str]
    completed: bool
    custom_fields: Optional[AsanaCustomFields]
    due_on: Optional[str]
    followers: Optional[str]
    name: str
    notes: Optional[str]
    projects: List[str]
    workspace: str


class AsanaProject(TypedDict):
    gid: str
    name: str
    color: str
    icon: str
    followers: str
    due_on: Optional[str]


class AsanaPortfolio(TypedDict):
    gid: str
    name: str
    resource_type: str
