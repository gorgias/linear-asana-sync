from flask import Blueprint, current_app, request

from src.sync import sync_asana_projects

default_blueprint = Blueprint("default", __name__)


@default_blueprint.route("/linear-asana-sync/", methods=("GET", "POST"))
def linear_projects():
    """Process Linear Projects Webhooks."""

    request_body = request.get_json(force=True)
    milestone_name = request_body["milestone_name"]
    if request_body:
        if milestone_name in current_app.config["LINEAR_MILESTONE_ASANA_PORTFOLIO"]:
            sync_asana_projects(milestone_name)
            return "Done"
        else:
            return f"Milestone name {milestone_name} was not found"
    else:
        return "Request body not found"
