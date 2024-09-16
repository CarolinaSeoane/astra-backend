from flask import Blueprint, g, request
from webargs import fields
from webargs.flaskparser import use_args
from bson import ObjectId

from app.models.team import Team
from app.models.user import User
from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.member import MemberStatus, Role

teams = Blueprint('teams', __name__)

excluded_routes = [
    {
        'route': '/teams/permissions',
        'methods': ['GET']
    },
    {
        'route': '/teams/join',
        'methods': ['GET']
    },
    {
        'route': '/teams/create',
        'methods': ['POST']
    }
]

@teams.before_request
def apply_validate_user_is_active_member_of_team():
    for excluded_route in excluded_routes:
        if request.path.startswith(excluded_route['route']) and (request.method in excluded_route['methods']):
            return None

    return validate_user_is_active_member_of_team()

@teams.route('/members', methods=['GET'])
def get_team_members():
    members = Team.get_team_members(g.team_id)
    return send_response(members, [], 200, **g.req_data)

def user_is_scrum_master_of_team(team_members, user_id):
    for member in team_members:
        if member['role'] == 'Scrum Master' and member['_id']['$oid'] == user_id: # TODO cahnge id to _id
            return True
    return False

new_member_schema = {
    'new_member_email': fields.Str(required=True), # user to be added
    'role': fields.Str(required=True)
}

@teams.route('/add_member', methods=['POST'])
@use_args(new_member_schema, location='json')
def add_team_member(args):
    '''
    Adds a member to the team with MemberStatus = ACTIVE.
    Also adds the team to the user's document with MemberStatus = ACTIVE
    '''
            
    members = Team.get_team_members(g.team_id)
    if user_is_scrum_master_of_team(members, g._id):
        new_member_email = args['new_member_email']
        user = User.get_user_by({'email': new_member_email})
        # print(f"adding user: {user}")
        if user is None:
            return send_response([], [f"No user found with email {new_member_email}"], 404, **g.req_data)
        if Team.is_user_part_of_team(user['_id']['$oid'], members):
            return send_response([], [f"User {new_member_email} is already a member of the team"], 400, **g.req_data)
        
        # users in team have: user_id, username, email, profile_picture, role, date
        user_obj = User(**user)
        # print(f"the user object: {user_obj.__dict__}")
        success = Team.add_member(g.team_id, user_obj, args['role'], MemberStatus.ACTIVE.value)
        if success:
            return send_response([], [], 200, **g.req_data)
        return send_response([], [f"Error adding user {new_member_email} to team"], 500, **g.req_data)
    else:
        return send_response([], ["User not authorized to complete operation"], 400, **g.req_data)

@teams.route('/remove_member/<member_id>', methods=['DELETE'])
def remove_team_member(member_id):
    members = Team.get_team_members(g.team_id)
    if user_is_scrum_master_of_team(members, g._id):
        Team.remove_member(g.team_id, member_id) # can a user remove themselves from a team? what happens if the team is empty after deletion?
        members = Team.get_team_members(g.team_id)
        print(f"team members after deletion: {members}")
        return send_response([], [], 200, **g.req_data)
    
    return send_response([], ["User not authorized to complete operation"], 400, **g.req_data)

@teams.route('/ceremonies', methods=['GET'])
def team_ceremonies():
    ceremonies = [
        {
            'name': 'Standup begins',
            'date': '2024-08-01T20:28:30',
            'in_progress': False
        },
        {
            'name': 'Standup',
            'date': '2024-08-01T20:28:35',
            'in_progress': True
        },
        {
            'name': 'Retro begins',
            'date': '2024-08-01T20:28:50',
            'in_progress': False
        },
        {
            'name': 'Retro',
            'date': '2024-08-01T20:28:55',
            'in_progress': True
        },
    ]
    
    return send_response(ceremonies, [], 200, **g.req_data)

@teams.route('/settings', methods=['GET'])
def get_team_settings():    
    team_settings = Team.get_team_settings(g.team_id)
    return send_response(team_settings, [], 200, **g.req_data)

@teams.route('/mandatory_fields', methods=['PUT'])
@use_args({'mandatory_fields': fields.List(fields.Str(), required=True)}, location='json')
def update_mandatory_fields(args):
    Team.update_mandatory_fields(g.team_id, args['mandatory_fields'])
    return send_response([], [], 200, **g.req_data)

@teams.route('/sprint_set_up', methods=['PUT'])
@use_args({
    'estimation_method': fields.List(fields.Str(required=False)),
    'sprint_duration': fields.Str(required=False),
    'sprint_begins_on': fields.Str(required=False)
    }, location='json')
def update_sprint_set_up(args):
    Team.update_sprint_set_up(g.team_id, args)
    return send_response([], [], 200, **g.req_data)

ceremony_args = {
    "days": fields.List(fields.Str(), required=True),
    "when": fields.Str(required=True),
    "time": fields.Str(required=True)
}

ceremonies_settings_args = {
    "planning": fields.Nested(ceremony_args, required=True),
    "standup": fields.Nested(ceremony_args, required=True),
    "retrospective": fields.Nested(ceremony_args, required=True)
}
@teams.route('/ceremonies_frequency', methods=['PUT'])
@use_args(ceremonies_settings_args, location='json')
def update_ceremonies_frequency(args):
    Team.update_ceremonies_settings(g.team_id, args)
    return send_response([], [], 200, **g.req_data)

permit_args = {
    'role': fields.Str(required=True),
    'options': fields.List(fields.Str(), required=True)
}
permissions_args = {
    'permits': fields.List(fields.Nested(permit_args), required=True)
}

@teams.route('/permissions', methods=['PUT'])
@use_args(permissions_args, location='json')
def update_permissions(args):
    Team.update_permissions(g.team_id, args['permits'])
    return send_response([], [], 200, **g.req_data)

@teams.route('/permissions', methods=['GET'])
def permissions():
    permissions = Team.get_base_permissions()
    return send_response(permissions, [], 200, **g.req_data)

@teams.route('/join/<team_id>', methods=['GET'])
def join_team_by_id(team_id):
    try:
        ObjectId(team_id)
    except:
        return send_response([], ['Invalid ID format'], 400, **g.req_data)

    team_to_join = Team.get_team(team_id)
    
    if not team_to_join:
        return send_response([], [f"Couldn't find a team with ID {team_id}"], 404, **g.req_data)
    
    team_members = Team.get_team_members(team_id)

    # if Team.is_user_part_of_team(g._id, team_members):
    if User.is_user_in_team(g._id, team_id):
        return send_response([], [f"User {g.email} is already a member of the team"], 400, **g.req_data)
    elif User.is_user_in_team(g._id, team_id, status=MemberStatus.PENDING.value):
        return send_response([f"You already sent a request to join {team_id}"], [], 200, **g.req_data)

    user = User.get_user_by({'email': g.email})
    user_obj = User(**user)
    success = Team.add_member(team_id, user_obj, None)
    
    if success:
        return send_response([f"Your request to join {team_id} was sent successfully"], [], 202, **g.req_data)
    
    return send_response([], [f"Error adding user {g.email} to team"], 500, **g.req_data)

@teams.route('/create', methods=['POST'])
@use_args({'team_name': fields.Str(required=True)}, location='json')
def create_team(args):
    user_doc = User.get_user_by({'email': g.email})
    user_obj = User(**user_doc)
    
    # Create team entity and add the user as Scrum Master
    new_team = {        
        "name": args['team_name'],
        # "organization": ,
        "google_meet_config": {
            "meeting_code": "",
            "meeting_space": ""
        },
        "members": [
            {
                "username": user_obj.username,
                "email": g.email,
                "profile_picture": user_obj.profile_picture,
                "role": Role.SCRUM_MASTER.value,
                "member_status": MemberStatus.ACTIVE.value
                # "date": self.user1_id.generation_time
            },
        ]
    }

    # Create meeting space for the team
    #
    #

    try:
        # Add new team
        res = Team.add_team(new_team)
        
        # Add team to user collection
        new_team = Team.get_team(res.inserted_id)
        user_obj.add_team(new_team, MemberStatus.ACTIVE.value)
    except Exception as e:
        print(e)
        return send_response([], ["Couldn't create team"], 500, **g.req_data)
  
    return send_response([f"Team {args['team_name']} created successfully"], [], 200, **g.req_data)
