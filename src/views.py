from flask import Blueprint
from src.commands import sync_asana_projects

linear_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@linear_blueprint.route("/linear-asana-sync/")
def linear_projects():
    """Process Linear Projects Webhooks. """

    sync_asana_projects()

    return "Done"
