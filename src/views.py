from flask import Blueprint

from src.sync import sync_asana_projects

default_blueprint = Blueprint("default", __name__)


@default_blueprint.route("/linear-asana-sync/")
def linear_projects():
    """Process Linear Projects Webhooks. """

    sync_asana_projects("Q2 2021")

    return "Done"
