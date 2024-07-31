from flask import Blueprint, request
from webargs import fields
from webargs.flaskparser import use_args
from bson import ObjectId

from app.services.token import validate_jwt
from app.models.team import Team
from app.models.user import User
from app.utils import send_response


teams = Blueprint('teams', __name__)

@teams.route('/get_members/<team_id>', methods=['GET']) # TODO change to /members/<team_id>
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
def get_team_members(headers, team_id):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    try:
        team_id = ObjectId(team_id)
    except:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **req_data)
    
    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)
    
    if not User.is_user_in_team(decoded['_id'], team_id):
        return send_response([], ["Forbidden. User is not authorized to access this resource"], 403, **req_data)
    
    members = Team.get_team_members(team_id)
    return send_response(members, [], 200, **req_data)

def user_is_scrum_master_of_team(team_members, user_id):
    for member in team_members:
        if member['role'] == 'Scrum Master' and member['_id']['$oid'] == user_id: # TODO cahnge id to _id
            return True
    return False

new_member_schema = {
    'new_member_email': fields.Str(required=True), # user to be added
    'role': fields.Str(required=True)
}

@teams.route('/add_member/<team_id>', methods=['POST'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
@use_args(new_member_schema, location='json')
def add_team_member(headers, args, team_id):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    try:
        team_id = ObjectId(team_id)
    except:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **req_data)

    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], ["Unauthorized. Invalid session token"], 401, **req_data)
    
    members = Team.get_team_members(team_id)
    if user_is_scrum_master_of_team(members, decoded['_id']):
        new_member_email = args['new_member_email']
        user = User.get_user_by({'email': new_member_email})
        print(f"adding user: {user}")
        if user is None:
            return send_response([], [f"No user found with email {new_member_email}"], 404, **req_data)
        if user['_id']['$oid'] in [member['_id']['$oid'] for member in members]: # TODO change id to _id
            return send_response([], [f"User {new_member_email} is already a member of the team"], 400, **req_data)
        
        # users in team have: user_id, username, email, profile_picture, role, date
        user_obj = User(**user)
        print(f"the user object: {user_obj.__dict__}")
        success = Team.add_member(team_id, user_obj, args['role'])
        if success:
            return send_response([], [], 200, **req_data)
        return send_response([], [f"Error adding user {new_member_email} to team"], 500, **req_data)
    else:
        return send_response([], ["User not authorized to complete operation"], 400, **req_data)

@teams.route('/remove_member/<team_id>/<member_id>', methods=['DELETE'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
def remove_team_member(headers, team_id, member_id):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    try:
        team_id = ObjectId(team_id)
    except:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **req_data)
    
    try:
        member_id = ObjectId(member_id)
    except:
        return send_response([], [f"Member id {member_id} is not valid"], 403, **req_data)

    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)
    user_id = decoded['_id']

    members = Team.get_team_members(team_id)
    if user_is_scrum_master_of_team(members, user_id):
        Team.remove_member(team_id, member_id) # can a user remove themselves from a team? what happens if the team is empty after deletion?
        members = Team.get_team_members(team_id)
        print(f"team members after deletion: {members}")
        return send_response([], [], 200, **req_data)
    
    return send_response([], ["User not authorized to complete operation"], 400, **req_data)

@teams.route('/settings/<team_id>', methods=['GET'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
def get_team_settings(headers, team_id):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    try:
        team_id = ObjectId(team_id)
    except:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **req_data)

    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)
    
    if not User.is_user_in_team(decoded['_id'], team_id):
        return send_response([], ["Forbidden. User is not authorized to access this resource"], 403, **req_data)
    
    team_settings = Team.get_team_settings(team_id)
    return send_response(team_settings, [], 200, **req_data)

@teams.route('/mandatory_fields/<team_id>', methods=['PUT'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
@use_args({'mandatory_fields': fields.List(fields.Str(), required=True)}, location='json')
def update_mandatory_fields(headers, args, team_id):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    try:
        team_id = ObjectId(team_id)
    except:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **req_data)

    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], ["Unauthorized. Invalid session token"], 401, **req_data)
    
    if not User.is_user_in_team(decoded['_id'], team_id):
        return send_response([], ["Forbidden. User is not authorized to access this resource"], 403, **req_data)

    Team.update_mandatory_fields(team_id, args['mandatory_fields'])
    return send_response([], [], 200, **req_data)

@teams.route('/sprint_set_up/<team_id>', methods=['PUT'])
@use_args({'Authorization': fields.Str(required=True)}, location='headers')
@use_args({
    'estimation_method': fields.List(fields.Str(), required=False),
    'sprint_duration': fields.Str(required=False),
    'sprint_begins_on': fields.Integer(required=False)
    }, location='json')
def update_sprint_set_up(headers, args, team_id):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    try:
        team_id = ObjectId(team_id)
    except:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **req_data)

    # Validate tokens
    decoded = validate_jwt(headers['Authorization'])   
    if not decoded:
        return send_response([], ["Unauthorized. Invalid session token"], 401, **req_data)
    
    if not User.is_user_in_team(decoded['_id'], team_id):
        return send_response([], ["Forbidden. User is not authorized to access this resource"], 403, **req_data)

    Team.update_sprint_set_up(team_id, args)
    return send_response([], [], 200, **req_data)

# @teams.route('/update_member_role/<team_id>/<member_id>', methods=['PUT'])