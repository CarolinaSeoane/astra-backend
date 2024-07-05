import os
import json
from flask import Blueprint, jsonify
from app.db_connection import mongo
from bson import json_util

teams = Blueprint("teams", __name__)

@teams.route("/")
def init_teams():
    list_cursor = list(mongo.db.movies.find(limit = 5))    
    response = json_util.dumps(list_cursor)    
    return response

