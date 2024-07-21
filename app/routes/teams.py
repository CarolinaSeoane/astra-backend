from flask import Blueprint, request
from webargs import fields
from webargs.flaskparser import use_args

from app.services.token import validate_jwt
from app.models.team import Team
from app.models.user import User
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
    
    # for member in members:
    #     if member['role'] == 'Scrum Master' and member['user']['$oid'] == args['user_id']:
    #         return send_response(members, [], 200, **req_data)

    if user_is_scrum_master_of_team(members, args['user_id']):
        return send_response(members, [], 200, **req_data)
    
    return send_response([], ["User not authorized to complete operation"], 400, **req_data)

def user_is_scrum_master_of_team(team_members, user_id):
    if team_members is None:
        return False
    
    for member in team_members:
        if member['role'] == 'Scrum Master' and member['user']['$oid'] == user_id:
            return True
    
    return False

new_member_schema = {
    'new_member_id': fields.Str(required=True), # user to be added
    'team_id': fields.Str(required=True), # team to add user to
    'role': fields.Str(required=True),
    'user_id': fields.Str(required=True) # user making the request
}

@teams.route('/add_member', methods=['POST'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
@use_args(new_member_schema, location='json')
def add_team_member(headers, args):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)
    
    members = Team.get_team_members(args["team_id"])
    if members is None:
        return send_response([], [f"No team found with id {args["team_id"]}"], 404, **req_data)
    
    if user_is_scrum_master_of_team(members, args['user_id']):
        # add new member to team
        new_member_id = args['new_member_id']
        user = User.get_user_by(new_member_id)
        if user is None:
            return send_response([], [f"No user found with id {new_member_id}"], 404, **req_data)
        if user['$oid'] in [member['user']['$oid'] for member in members]:
            return send_response([], [f"User {new_member_id} is already a member of the team"], 400, **req_data)
        
        # users in team have: user_id, username, email, profile_picture, role, date
        user_obj = User(**user)
        
        Team.add_member(args["team_id"], user_obj)
        
        return send_response([], [], 200, **req_data)


@teams.route('/remove_member/<member_id>', methods=['DELETE'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
@use_args({'user_id': fields.Str(required=True)}, location='json')
def remove_team_member(headers, args, team_id):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)
    
