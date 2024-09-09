from flask import Blueprint, request
from webargs import fields
from webargs.flaskparser import use_args
from bson import json_util
import json
from app.services.google_auth import validate_credentials
from app.services.token import generate_jwt
from app.models.user import User
from app.utils import send_response


users = Blueprint('users', __name__)

@users.route('/login', methods=['POST'])
@use_args({'access_token': fields.Str(required=True),
           'authuser': fields.Str(required=True),
           'expires_in': fields.Integer(required=True),
           'prompt': fields.Str(required=True),
           'scope': fields.Str(required=True),
           'hd': fields.Str(required=False),
           'token_type': fields.Str(required=True)}, location='json')
def handle_login(args):
    # TODO: handle already existing jwt?

    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }
    
    try:
        id_info = validate_credentials(args['access_token'])
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
                "surname": family_name
            }
        return send_response(data, ["User not found. Please complete the sign-up process."], 404, **req_data)
    else:
        # User is signed up and we only need to log them in
        session_token = generate_jwt(email, user['_id']['$oid'])
        data = {
            "user": user,
            "token": session_token
        }
        return send_response(data, [], 200, **req_data)


@users.route('/sign-up', methods=['POST'])
@use_args({'name': fields.Str(required=True),
           'surname': fields.Str(required=True),
           'email': fields.Str(required=True),
           'username': fields.Str(required=True),
           'profile_picture': fields.Str(required=True)}, location='json')
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
    
    data = {
        "user": new_user_dict,
        "token": session_token
    }

    return send_response(data, [], 201, **req_data)
