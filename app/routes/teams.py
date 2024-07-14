import json
from flask import Blueprint, jsonify
from app.db_connection import mongo
from bson import json_util

teams = Blueprint("teams", __name__)

@teams.route("/")
def init_teams():
    list_cursor = list(mongo.db.movies.find(limit = 5))    
    response = json_util.dumps(list_cursor) #this serializes MongoDB documents (which are Python dictionaries) into a JSON-encoded string.
    # print(type(json.loads(response)[0])) We are returning a JSON a list of <class 'dict'>
    response = json.loads(response) # This function deserializes (parses) a JSON string into a Python object, typically a dictionary or a list of dictionaries.

    return jsonify("hola mundo"), 200
