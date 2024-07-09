import os
from flask import Blueprint, jsonify

index = Blueprint("index", __name__)


@index.route("/")
def init_teams():
    print(f"in the route {os.environ.get('FLASK_APP')}")

    return jsonify("Hello World (from the index page!)"), 200
