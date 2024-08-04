from flask import Blueprint, request, g
from bson import ObjectId
from webargs import fields
from webargs.flaskparser import use_args

from app.models.story import Story
from app.utils import send_response
from app.models.user import User


stories = Blueprint("stories", __name__)

@stories.route("/<view_type>/<team_id>", methods=['GET'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
def stories_list(args, team_id, view_type): 
    try:
        team_id = ObjectId(team_id)
    except Exception:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **g.req_data)
    
    # Validate if user is part of the team
    if not User.is_user_in_team(g._id, team_id):
        return send_response([], [f"Forbidden. User is not authorized to access this resource"], 403, **g.req_data)

    stories = Story.get_stories_by_team_id(team_id, view_type)

    return send_response(stories, [], 200, **g.req_data)

@stories.route("/fields", methods=['GET'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
def story_fields(args):
    fields = Story.get_story_fields()
    return send_response(fields, [], 200, **g.req_data)
