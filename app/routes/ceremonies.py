from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from bson import ObjectId
from app.db_connection import mongo
from app.routes.utils import validate_user_is_member_of_team

ceremonies = Blueprint("ceremonies", __name__)

excluded_routes = []

@ceremonies.before_request
def apply_validate_user_is_member_of_team():
    if any(request.path.startswith(route) for route in excluded_routes):
        return None
    return validate_user_is_member_of_team()

# Ruta para crear una nueva ceremonia
@ceremonies.route("/", methods=['POST'])
@use_args({'name': fields.Str(required=True), 'start_time': fields.Str(required=True)}, location='json')
def add_ceremony(args):
    name = args.get('name')
    start_time = args.get('start_time')
    team_id = request.args.get('team_id')

    if not name or not start_time or not team_id:
        return jsonify({"error": "name, start_time, and team_id are required"}), 400

    new_ceremony = {
        "name": name,
        "start_time": start_time,
        "team_id": team_id
    }

    try:
        result = mongo.db.ceremonies.insert_one(new_ceremony)
        new_ceremony['_id'] = str(result.inserted_id)
        return jsonify(new_ceremony), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar la hora de una ceremonia
@ceremonies.route("/<ceremony_id>/time", methods=['PUT'])
@use_args({'new_time': fields.Str(required=True)}, location='json')
def update_ceremony_time(args, ceremony_id):
    new_time = args.get('new_time')
    team_id = request.args.get('team_id')

    if not team_id:
        return jsonify({"error": "team_id is required"}), 400

    if not ObjectId.is_valid(ceremony_id):
        return jsonify({"error": "Invalid ceremony_id"}), 400

    try:
        result = mongo.db.ceremonies.update_one(
            {"_id": ObjectId(ceremony_id), "team_id": team_id},
            {"$set": {"start_time": new_time}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Ceremony not found"}), 404
        
        return jsonify({"message": "Ceremony time updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500