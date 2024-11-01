import json
from flask import Blueprint, request, g
from webargs import fields
from webargs.flaskparser import use_args
from bson import json_util, ObjectId

from app.services.google_auth import validate_credentials, exchange_code_for_tokens
from app.services.token import generate_jwt
from app.models.user import User
from app.utils import send_response
from app.models.sprint import Sprint
from app.models.story import Story


users = Blueprint('users', __name__)

@users.route('/login', methods=['POST'])
@use_args({'auth_code': fields.Str(required=True)}, location='json')
def handle_login(args):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    try:
        tokens = exchange_code_for_tokens(args['auth_code'])
        id_info = validate_credentials(tokens['access_token'])
    except ValueError as err:
        # Invalid token 
        print(err)
        return send_response([], ["Unauthorized. Access is denied due to invalid credentials."], 401, **req_data)

    # ID token is valid
    email = id_info['email']
    family_name = id_info['family_name']
    name = id_info['name'].replace(family_name, '').strip()

    # Get user from db
    user = User.get_user_by({'email': email})

    if user is None:
        # User is not in our db and we need to redirect them to the sign up screen
        data = {
                "email": email,
                "name": name,
                "surname": family_name,
                "access_token": tokens['access_token'],
                "refresh_token": tokens['refresh_token'],
            }
        return send_response(data, ["User not found. Please complete the sign-up process."], 404, **req_data)
    else:
        # User is signed up and we only need to log them in and update their access token
        User.update_access_token(user['_id']['$oid'], tokens['access_token'])

        session_token = generate_jwt(email, user['_id']['$oid'])
        user['token'] = session_token
        data = {
            "user": user,
        }
        return send_response(data, [], 200, **req_data)


@users.route('/sign-up', methods=['POST'])
@use_args({'name': fields.Str(required=True),
           'surname': fields.Str(required=True),
           'email': fields.Str(required=True),
           'username': fields.Str(required=True),
           'profile_picture': fields.Str(required=True),
           'access_token': fields.Str(required=True),
           'refresh_token': fields.Str(required=True)}, location='json')
def sign_up(args):
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    # Verify email doesn't exist
    user = User.get_user_by({'email': args['email']})
    if user is not None:
        return send_response([], [f"Conflict. A user with the email {args['email']} already exists."], 409, **req_data)

    # Email doesn't exist. Save user to mongo
    new_user = User(**args)

    new_user.save_user()
    session_token = generate_jwt(args['email'], str(new_user._id))

    new_user_str = json_util.dumps(new_user.__dict__)
    new_user_dict = json.loads(new_user_str)
    new_user_dict['token'] = session_token

    return send_response(new_user_dict, [], 201, **req_data)

@users.route('/context/<user_id>', methods=['GET'])
def refresh_context(user_id):
    # Get user from db
    user = User.get_user_by({'_id': ObjectId(user_id)})

    if not user:
        return send_response([], ['Invalid user _id. Login again'], 401, **g.req_data)

    session_token = generate_jwt(g.email, user['_id']['$oid'])
    user['token'] = session_token

    return send_response(user, [], 200, **g.req_data)

@users.route("/velocity", methods=['GET'])
@use_args({'team_id': fields.Str(required=True), 'user_id': fields.Str(required=True)}, location='query')
def response_velocity(args):
    team_id =  args.get('team_id') #g.team_id NO
    user_id =  args.get('user_id') #g._id 

    velocity_data, average_velocity = data_velocity(team_id, user_id)
    data = {
        "velocity_data": velocity_data,
        "average_velocity": average_velocity
    }

    message = "Request successful"
    return send_response(data, message, 200, **g.req_data)

def data_velocity(team_id, user_id):
    sprints = Sprint.get_active_sprints(team_id)

    if not sprints:
        return [], 0

    velocity_data = []
    total_completed = 0
    total_sprints = 0

    for sprint in sprints:
        sprint_name = sprint['name']
        stories = Story.get_stories_by_team_id(
            ObjectId(team_id),
            view_type='list',
            sprint=sprint['name'],
            assigned_to=user_id
        )

        if not stories:
            continue  # Skip this sprint if there are no stories

        sprint_target = 0
        sprint_completed = 0

        for story in stories:
            try:
                estimation = int(story['estimation'])
                sprint_target += estimation

                if story.get('completeness', 0) == 100:
                    sprint_completed += estimation
            except (ValueError, TypeError):
                continue

        if sprint_target > 0:
            velocity_data.append({
                'name': sprint_name,
                'target': sprint_target,
                'completed': sprint_completed
            })
            total_completed += sprint_completed
            total_sprints += 1

    average_velocity = total_completed / total_sprints if total_sprints > 0 else 0

    return velocity_data, average_velocity

@users.route('/completed_stories', methods=['GET'])
def completed_stories():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')

    if not user_id or not team_id:
        return send_response(None, "Missing team_id or user_id", 400, **g.req_data)

    # all active sprints of team
    active_sprints = Sprint.get_active_sprints(team_id)

    if not active_sprints:
        data = [
            {'value': 0, 'name': "Late"},
            {'value': 0, 'name': "Total stories"}
        ]
        return send_response(data, "No active sprints found", 200, **g.req_data)

    total_stories = 0
    incomplete_stories = 0

    for sprint in active_sprints:
        sprint_id = str(sprint['_id']['$oid'])
        #print("sprint_id", sprint_id)

        sprint_total, sprint_incomplete = Sprint.count_stories(sprint_id, team_id, user_id)

        total_stories += sprint_total
        incomplete_stories += sprint_incomplete

    data = [
        { 'value': incomplete_stories, 'name': "Late" },
        { 'value': total_stories, 'name': "Total stories" }
    ]

    #print(f"Total Stories: {total_stories}, Incomplete Stories: {incomplete_stories}")

    return send_response(data, "Success", 200, **g.req_data)
