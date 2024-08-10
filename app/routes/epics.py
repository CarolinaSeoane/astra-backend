import os
from bson import ObjectId
from flask import Blueprint, request, jsonify, g
from webargs import fields
from app.db_connection import mongo
from app.services.token import validate_jwt

epics = Blueprint('epics', __name__)

# Validación para la creación de epics
epic_args = {
    'title': fields.Str(required=True),
    'description': fields.Str(required=True),
    'sprints': fields.Str(required=True),
    'priority': fields.Str(required=True),
}

# Validación para la actualización de epics
update_epic_args = {
    'description': fields.Str(required=False),
    'sprints': fields.Str(required=False),
    'priority': fields.Str(required=False),
}

def get_current_user(request):
    if os.getenv('DEVELOPMENT_MODE', 'False') == 'True':
        return {'sub': 'simulated_user_id', 'username': 'Usuario de prueba', 'email': 'test@example.com', 'picture': 'default.png'}
    
    token = request.headers.get('Authorization', None)
    if token is None:
        print("No token provided")
        return None

    token = token.replace('Bearer ', '')
    decoded = validate_jwt(token)
    if 'error' in decoded:
        print(f"Token validation error: {decoded['error']}")
        return None

    user_id = decoded.get('_id')
    if user_id is None:
        print("No _id in JWT")
        return None

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        print(f"User not found in database for ID: {user_id}")
        return None

    return {
        'sub': user.get('_id', str(user_id)),
        'username': user.get('username', 'Unknown'),
        'email': user.get('email', ''),
        'picture': user.get('profile_picture', '')
    }
    
def convert_objectid_to_str(document):
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, list):
                document[key] = [convert_objectid_to_str(i) for i in value]
            elif isinstance(value, dict):
                document[key] = convert_objectid_to_str(value)
    return document

@epics.route('/', methods=['POST'])
def create_epic():
    current_user = get_current_user(request)
    if current_user is None:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        args = request.get_json()
        
        # Normalizar el título
        normalized_title = args['title'].strip().lower()
        
        # Comprobar si ya existe una épica con el mismo título normalizado
        existing_epic = mongo.db.epics.find_one({"title": normalized_title, "creator._id": current_user['sub']})
        if existing_epic:
            return jsonify({"error": "Epic with this title already exists."}), 400

        creator_data = {
            "_id": current_user['sub'],  
            "username": current_user.get('username', 'Unknown'),  
            "profile_picture": current_user.get('picture', '') 
        }
        
        # Preparar los datos de la épica para la inserción
        epic_data = {
            'title': args['title'],
            'description': args.get('description', ''),
            'sprints': args.get('sprints', ''),
            'priority': args.get('priority', ''),
            'creator': creator_data
        }
        result = mongo.db.epics.insert_one(epic_data)
        created_epic = mongo.db.epics.find_one({"_id": result.inserted_id})
        created_epic = convert_objectid_to_str(created_epic) 
        return jsonify(created_epic), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@epics.route('/<string:title>', methods=['PUT'])
def update_epic(title):
    current_user = get_current_user(request)
    if current_user is None:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        args = request.get_json()
        
        epic = mongo.db.epics.find_one({"title": title})
        if not epic:
            return jsonify({"message": "Epic not found."}), 404

        creator_id = epic.get('creator', {}).get('_id', None)
        if creator_id != current_user['sub']:
            return jsonify({"message": "Unauthorized to update this epic."}), 403

        update_fields = {key: value for key, value in args.items() if value is not None}

        if update_fields:
            result = mongo.db.epics.update_one({"title": title}, {"$set": update_fields})
            if result.matched_count == 0:
                return jsonify({"message": "Epic update failed."}), 500

        updated_epic = mongo.db.epics.find_one({"title": title})
        if updated_epic:
            updated_epic = convert_objectid_to_str(updated_epic)
            return jsonify(updated_epic), 200
        else:
            return jsonify({"message": "Epic update failed."}), 500

    except Exception as e:
        print(f"Exception: {e}") 
        return jsonify({"error": str(e)}), 500

@epics.route('/', methods=['GET'])
def get_all_epics():
    current_user = get_current_user(request)
    if current_user is None:
        return jsonify({"message": "Unauthorized"}), 401
    
    try:
        epics_list = mongo.db.epics.find({"creator._id": current_user['sub']})
        epics_data = [convert_objectid_to_str(epic) for epic in epics_list]
        return jsonify(epics_data), 200
    except Exception as e:
        print(f"Exception: {e}")  
        return jsonify({"error": str(e)}), 500
