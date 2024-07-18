import json
from flask import Blueprint, jsonify
from bson import ObjectId
from webargs import fields
from webargs.flaskparser import use_args

from app.db_connection import mongo
from app.models.story import Story

stories = Blueprint("stories", __name__)

@stories.route("/list/<team_id>", methods=['GET'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
def stories_list(args, team_id):
    try:
        team_id = ObjectId(team_id)
    except Exception as e:
        return jsonify(f"Team id {team_id} is not valid"), 403
    
    stories = Story.get_stories_by_team_id(team_id)

    return jsonify(stories), 200
