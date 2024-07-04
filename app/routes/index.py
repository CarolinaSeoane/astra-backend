from flask import Blueprint, jsonify

index = Blueprint("index", __name__)

@index.route("/")
def init_teams():
    return jsonify("Hello World (from the index page!)", 200)
