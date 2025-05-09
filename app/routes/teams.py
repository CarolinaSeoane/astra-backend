from flask import Blueprint, g, request
from webargs import fields
from webargs.flaskparser import use_args
from bson import ObjectId

from app.models.team import Team
from app.models.user import User
from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.configurations import Configurations, MemberStatus, Role, CeremonyType
from app.models.organization import Organization
from app.models.sprint import Sprint


teams = Blueprint('teams', __name__)

VALIDATE_SECTIONS = [
    'ceremonies',
    'sprint_set_up',
    'mandatory_story_fields',
    'permits',
    'estimation_method'
]
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
        if (
            request.path.startswith(excluded_route['route'])
            and (request.method in excluded_route['methods'])
        ):
            return None

    return validate_user_is_active_member_of_team()

@teams.route('/members', methods=['GET'])
def get_team_members():
    members = Team.get_team_members(g.team_id)
    return send_response(members, [], 200, **g.req_data)

def user_is_scrum_master_of_team(team_members, user_id):
    for member in team_members:
        if member['role'] == 'Scrum Master' and member['_id']['$oid'] == user_id:
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
            return send_response(
                [], [f"No user found with email {new_member_email}"], 404, **g.req_data
            )
        if Team.is_user_part_of_team(user['_id']['$oid'], members):
            return send_response(
                [], [f"User {new_member_email} is already a member of the team"], 400, **g.req_data
            )

        # users in team have: user_id, username, email, profile_picture, role, date
        user_obj = User(**user)
        success = Team.add_member(g.team_id, user_obj, args['role'], MemberStatus.ACTIVE.value)
        if success:
            return send_response([], [], 200, **g.req_data)
        return send_response(
            [], [f"Error adding user {new_member_email} to team"], 500, **g.req_data
        )
    else:
        return send_response([], ["User not authorized to complete operation"], 400, **g.req_data)

# Validate query param
def validate_section(value):
    if value not in VALIDATE_SECTIONS:
        raise ValueError(f"Invalid section value. Must be one of: {', '.join(VALIDATE_SECTIONS)}")

@teams.route('/settings', methods=['GET'])
@use_args({'section': fields.Str(required=False, validate=validate_section)}, location='query')
def get_team_settings(args):
    team_settings = Team.get_team_settings(g.team_id, args.get('section'))
    return send_response(team_settings, [], 200, **g.req_data)

@teams.route('/mandatory_fields', methods=['PUT'])
@use_args({'mandatory_fields': fields.List(fields.Str(), required=True)}, location='json')
def update_mandatory_fields(args):
    Team.update_mandatory_fields(g.team_id, args['mandatory_fields'])
    return send_response([], [], 200, **g.req_data)

@teams.route('/sprint_set_up', methods=['PUT'])
@use_args({
    'sprint_duration': fields.Integer(required=True),
    'sprint_begins_on': fields.Str(required=True)
    }, location='json')
def update_sprint_set_up(args):
    Team.update_sprint_set_up(g.team_id, args)
    return send_response([], [], 200, **g.req_data)

ceremony_args = {
    "days": fields.List(fields.Str(), required=False),
    "when": fields.Str(required=False),
    "starts": fields.Str(required=True),
    "ends": fields.Str(required=True),
    "google_meet_config": fields.Dict(required=False),
}

@teams.route('/ceremonies', methods=['PUT'])
@use_args({
    "planning": fields.Nested(ceremony_args, required=True),
    "standup": fields.Nested(ceremony_args, required=True),
    "retrospective": fields.Nested(ceremony_args, required=True)
}, location='json')
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
    base_permissions = Team.get_base_permissions()
    return send_response(base_permissions, [], 200, **g.req_data)

@teams.route('/join/<team_id>', methods=['GET'])
def join_team_by_id(team_id):
    try:
        ObjectId(team_id)
    except Exception:
        return send_response([], ['Invalid ID format'], 400, **g.req_data)

    team_to_join = Team.get_team(team_id)

    if not team_to_join:
        return send_response([], [f"Couldn't find a team with ID {team_id}"], 404, **g.req_data)

    # team_members = Team.get_team_members(team_id)
    # if Team.is_user_part_of_team(g._id, team_members):
    if User.is_user_in_team(g._id, team_id):
        return send_response(
            [], [f"User {g.email} is already a member of the team"], 400, **g.req_data
        )
    elif User.is_user_in_team(g._id, team_id, status=MemberStatus.PENDING.value):
        return send_response(
            [f"You already sent a request to join {team_id}"], [], 200, **g.req_data
        )

    user = User.get_user_by({'email': g.email})
    user_obj = User(**user)
    success = Team.add_member(team_id, user_obj, None)

    if success:
        return send_response(
            [f"Your request to join {team_id} was sent successfully"], [], 202, **g.req_data
        )
    return send_response([], [f"Error adding user {g.email} to team"], 500, **g.req_data)

@teams.route('/create', methods=['POST'])
@use_args({'team_name': fields.Str(required=True)}, location='json')
def create_team(args):
    user_doc = User.get_user_by({'email': g.email}, True)
    user_obj = User(**user_doc)

    # Create team entity and add the user as Scrum Master
    org = Organization.get_organization_by({'name': 'UTN'})
    new_team = {
        "name": args['team_name'],
        "organization": org['_id'],
        "members": [
            {
                "_id": ObjectId(g._id),
                "username": user_obj.username,
                "email": g.email,
                "profile_picture": user_obj.profile_picture,
                "role": Role.SCRUM_MASTER.value,
                "member_status": MemberStatus.ACTIVE.value
                # "date": self.user1_id.generation_time
            },
        ]
    }

    try:
        # Add new team
        res = Team.add_team(new_team)

        # Add team to user collection
        new_team = Team.get_team(res.inserted_id)
        new_team_id = new_team['_id']['$oid']
        user_obj.add_team(new_team, MemberStatus.ACTIVE.value)

        # Create backlog (every team starts with an active backlog)
        Sprint.create_backlog_for_new_team(res.inserted_id)

        # Create default team settings
        Team.add_default_settings(new_team_id)
        print('after team settings')
        # Add Google Meet space to each ceremony
        Team.set_up_google_meet_space(
            new_team_id, CeremonyType.STANDUP.value, user_obj.access_token, user_obj.refresh_token
        )
        Team.set_up_google_meet_space(
            new_team_id, CeremonyType.PLANNING.value, user_obj.access_token, user_obj.refresh_token
        )
        Team.set_up_google_meet_space(
            new_team_id, CeremonyType.RETRO.value, user_obj.access_token, user_obj.refresh_token
        )
    except Exception as e:
        print(e)
        #TODO: rollback
        return send_response([], ["Couldn't create team"], 500, **g.req_data)

    return send_response([f"Team {args['team_name']} created successfully"], [], 200, **g.req_data)

@teams.route('/member_role', methods=['GET'])
@use_args({"team_id": fields.Str(required=True)}, location='query')
def get_member_role(args):
    team_id = args["team_id"]
    user = User.get_user_by({"_id": ObjectId(g._id)})
    role = Team.get_member_role(team_id, user["email"])
    return send_response(role, [], 200, **g.req_data)

@teams.route('/permissions_by_role/<role>', methods=['GET'])
@use_args({"team_id": fields.Str(required=True)}, location='query')
def get_permissions_based_on_role(args, role):
    team_id = args["team_id"]
    role = role.replace("_", " ")
    if role == Role.SCRUM_MASTER.value:
        permissions_label = Configurations.get_permissions_label(Role.SCRUM_MASTER.value)
    else:
        permissions_value = Team.get_permissions_value_based_on_role(team_id, role)
        permissions_label = Configurations.get_permissions_label(role, permissions_value)
    return send_response(permissions_label, [], 200, **g.req_data)

@teams.route('/is_member_allowed/<role>/<action>')
def is_member_allowed(role, action):
    """
    Scrum Masters are allowed to perform all actions
    """
    if role == Role.SCRUM_MASTER.value:
        return send_response(True, [], 200, **g.req_data)

    allowed = Team.is_member_authorized(g.team_id, role, action)
    return send_response(allowed, [], 200, **g.req_data)

roles_args = {
    "_id": fields.Str(required=True),
    "role": fields.Str(required=True),
}

@teams.route('/roles', methods=['PUT'])
@use_args({'roles': fields.List(fields.Nested(roles_args), required=True)}, location='json')
def new_roles(args):
    Team.update_members_role(g.team_id, args["roles"])
    return send_response([], [], 200, **g.req_data)

@teams.route('/pending/accept/<user_email>', methods=['PUT'])
def accept_pending_member(user_email):
    Team.accept_member(user_email, g.team_id)
    return send_response([], [], 200, **g.req_data)

@teams.route('/remove_member/<member_id>', methods=['DELETE'])
def remove_team_member(member_id):
    # members = Team.get_team_members(g.team_id)
    # if user_is_scrum_master_of_team(members, g._id):
    Team.remove_member(g.team_id, member_id) # can a user remove themselves from a team? what happens if the team is empty after deletion?
    # members = Team.get_team_members(g.team_id)
    # print(f"team members after deletion: {members}")
    return send_response([], [], 200, **g.req_data)
    # return send_response([], ["User not authorized to complete operation"], 400, **g.req_data)
