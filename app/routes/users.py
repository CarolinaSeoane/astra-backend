from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from app.services.google_auth import validate_credentials
from app.services.token import generate_jwt
from app.models.user import User

users = Blueprint('users', __name__)

@users.route('/login', methods=['POST'])
@use_args({'credential': fields.Str(required=True)}, location='json')
def handle_login(args):
    # TODO: handle already existing jwt?
    try:
        id_info = validate_credentials(args['credential'])
    except ValueError as err:
        # Invalid token 
        print(err)
        return jsonify({"message": "Unauthorized. Access is denied due to invalid credentials."}), 401
    
    # ID token is valid
    email = id_info['email']
    family_name = id_info['family_name']
    name = id_info['name'].replace(family_name, '').strip()
    
    # Get user from db
    user = User.get_user(email)

    if user is None:
        # User is not in our db and we need to redirect them to the sign up screen
        return jsonify({
            "message": "User not found. Please complete the sign-up process.",
            "data": {
                "email": email,
                "name": name,
                "surname": family_name
            }
        }), 404
    else:
        # User is signed up and we only need to log them in
        session_token = generate_jwt(email, str(user._id))
        return jsonify({
            "message": "User logged in successfully.",
            "data": user.from_obj_to_dict(),
            "token": session_token
        }), 200

@users.route('/sign-up', methods=['POST'])
@use_args({'name': fields.Str(required=True),
           'surname': fields.Str(required=True),
           'email': fields.Str(required=True),
           'username': fields.Str(required=True),
           'profile_picture': fields.Str(required=True)}, location='json')
def sign_up(args):

    # Verify email doesn't exist
    user = User.get_user(args['email'])
    if user is not None:
        return jsonify({
            "message": f"Conflict. A user with the email {args['email']} already exists."
        }), 409
 
    # Email doesn't exist. Save user to mongo
    new_user = User(**args)
    new_user.save_user()
    session_token = generate_jwt(args['email'], "str(new_user._id)")
    
    return jsonify({
        "message": "User signed up successfully.",
        "data": new_user.from_obj_to_dict(),
        "token": session_token
    }), 201
