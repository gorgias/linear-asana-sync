from flask import Flask

from src.commands import sync_commands
from src.views import default_blueprint


def create_app() -> Flask:
    """Flask App factory"""

    flask_app = Flask(__name__)
    flask_app.config.from_pyfile("config.py")
    flask_app.cli.add_command(sync_commands)
    flask_app.register_blueprint(default_blueprint)

    return flask_app


app = create_app()
