from flask import Blueprint, request
from webargs import fields
from webargs.flaskparser import use_args
from bson import ObjectId

from app.services.token import validate_jwt
from app.models.team import Team
from app.utils import send_response


teams = Blueprint('teams', __name__)

@teams.route('/get_members/<team_id>', methods=['GET'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
@use_args({'user_id': fields.Str(required=True)}, location='json')
def get_team_members(headers, args, team_id):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)

    # we verify the requesting user is indeed the scrum master of the team
    members = Team.get_team_members(team_id)
    if members is None:
        return send_response([], [f"No team found with id {team_id}"], 404, **req_data)
    
    for member in members:
        if member['role'] == 'Scrum Master' and member['user']['$oid'] == args['user_id']:
            return send_response(members, [], 200, **req_data)
    
    return send_response([], ["User not authorized to complete operation"], 400, **req_data)
