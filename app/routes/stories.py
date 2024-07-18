from flask import Blueprint, request
from bson import ObjectId
from webargs import fields
from webargs.flaskparser import use_args

from app.models.story import Story
from app.utils import send_response


stories = Blueprint("stories", __name__)

@stories.route("/list/<team_id>", methods=['GET'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
def stories_list(args, team_id):
    route = request.path
    method = request.method
    # validate credential
    try:
        team_id = ObjectId(team_id)
    except Exception:
        return send_response(route, method, [], [f"Team id {team_id} is not valid"], 403)
    
    stories = Story.get_stories_by_team_id(team_id)

    return send_response(route, method, stories, [], 200)
