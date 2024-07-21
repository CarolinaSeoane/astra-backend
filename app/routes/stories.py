from flask import Blueprint, request
from bson import ObjectId
from webargs import fields
from webargs.flaskparser import use_args

from app.models.story import Story
from app.utils import send_response
from app.services.token import validate_jwt
from app.models.user import User


stories = Blueprint("stories", __name__)

@stories.route("/list/<team_id>", methods=['GET'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
def stories_list(args, team_id):
    
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    # Validate token
    decoded = validate_jwt(args['Authorization'])
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)

    try:
        team_id = ObjectId(team_id)
    except Exception:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **req_data)
    
    # Validate if user is part of the team
    if not User.is_user_in_team(decoded['_id'], team_id):
        return send_response([], [f"Forbidden. User is not authorized to access this resource"], 403, **req_data)


    stories = Story.get_stories_by_team_id(team_id)

    return send_response(stories, [], 200, **req_data)
