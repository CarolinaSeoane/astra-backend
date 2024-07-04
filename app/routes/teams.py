from flask import Blueprint, jsonify

teams = Blueprint("teams", __name__)

@teams.route("/")
def init_teams():
    return jsonify("Hello World (from the teams page!)", 200)
