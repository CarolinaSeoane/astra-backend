from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from app.db_connection import mongo 
from app.services.token import validate_jwt 

ceremonies = Blueprint('ceremonies', __name__)

@ceremonies.route('/<ceremony_id>/attendees', methods=['PUT'])
def confirm_attendance(ceremony_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token is missing or invalid'}), 401

    token = auth_header.split(' ')[1]
    decoded = validate_jwt(token)
    if 'error' in decoded:
        return jsonify({'error': decoded['error']}), 401

    data = request.get_json()
    user_id = data.get('user_id')
    justification = data.get('justification', "")

    # Encuentra la ceremonia por ID
    ceremonies_collection = mongo.db.ceremonies
    ceremony = ceremonies_collection.find_one({"_id": ObjectId(ceremony_id)})
    if not ceremony:
        return jsonify({"error": "Ceremony not found"}), 404

    # Añadir asistente a la ceremonia
    attendees = ceremony.get('attendees', [])
    attendees.append({
        "user_id": user_id,
        "justification": justification
    })

    # Actualizar la ceremonia en la base de datos
    ceremonies_collection.update_one(
        {"_id": ObjectId(ceremony_id)},
        {"$set": {"attendees": attendees}}
    )

    return jsonify({"message": "Attendance confirmed successfully"}), 200