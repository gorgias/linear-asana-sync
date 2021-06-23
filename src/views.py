from flask import Blueprint, current_app

from src.sync import sync_asana_projects

default_blueprint = Blueprint("default", __name__)


@default_blueprint.route("/linear-asana-sync/")
def linear_projects():
    """Process Linear Projects Webhooks. """

    for portfolio_name, _ in current_app.config['LINEAR_MILESTONE_ASANA_PORTFOLIO'].items():
        sync_asana_projects(portfolio_name)

    return "Done"
