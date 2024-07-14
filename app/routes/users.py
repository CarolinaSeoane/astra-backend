from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from app.services.google_auth import validate_credentials
from app.services.db import get_user

users = Blueprint('users', __name__)

@users.route('/login', methods=['POST'])
@use_args({'credential': fields.Str(required=True)}, location='json')
def handleLogin(args):
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
    user = get_user(email)

    if user is None:
        # User is not in our db and we need to redirect them to the sign up screen
        return jsonify({
            "message": "User not found. Please complete the sign-up process.",
            "email": email,
            "name": name,
            "surname": family_name
        }), 404
    else:
        # User is signed up and we only need to log them in
        # To-Do: manage sessions
        return jsonify({
            "message": "User logged in successfully.",
            "user": user['name'] #To-Do
        }), 200

