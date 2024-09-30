from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from app.models.post_it import PostIt
from app.db_connection import mongo
from app.routes.utils import validate_user_is_active_member_of_team  
from bson import ObjectId
import traceback
from datetime import datetime, timedelta

post_its = Blueprint("post_its", __name__)

excluded_routes = []

@post_its.before_request
def apply_validate_user_is_active_member_of_team():
    if any(request.path.startswith(route) for route in excluded_routes):
        return None
    return validate_user_is_active_member_of_team()

#def is_editing_allowed(team_id, ceremony_id):
def is_editing_allowed(team_id):
    """
    Function to check if editing is allowed based on current time.
    Editing is allowed only 10 minutes before the ceremony starts 
    and disallowed when the ceremony starts.
    """
    
    #ceremony_data = mongo.db.ceremonies.find_one({"_id": ObjectId(ceremony_id), "team_id": team_id})
    
    #if not ceremony_data or "start_time" not in ceremony_data:
    #    return False 

    #ceremony_start_time = ceremony_data["start_time"]

    #current_time = datetime.now()
    #editing_start_time = ceremony_start_time - timedelta(minutes=10)
    #editing_end_time = ceremony_start_time

    #return editing_start_time <= current_time <= editing_end_time
    return True

@post_its.route("/", methods=['GET'])
@use_args({'team_id': fields.Str(required=True)}, location='query')
#@use_args({'team_id': fields.Str(required=True), 'ceremony_id': fields.Str(required=True)}, location='query')
def get_post_its(args):
    team_id = args.get('team_id')
    #ceremony_id = args.get('ceremony_id')
    if not team_id:
        return jsonify({"error": "team_id is required"}), 400
    #if not team_id or not ceremony_id:
    #    return jsonify({"error": "team_id and ceremony_id are required"}), 400
    post_its_cursor = mongo.db.post_its.find({"team_id": team_id})
    #post_its_cursor = mongo.db.post_its.find({"team_id": team_id, "ceremony_id": ceremony_id})
    post_its = list(post_its_cursor)

    for post_it in post_its:
        post_it['_id'] = str(post_it['_id'])

    return jsonify(post_its)

@post_its.route("/", methods=['POST'])
@use_args({'content': fields.Str(required=True), 'category': fields.Str(required=True)}, location='json')
#@use_args({'content': fields.Str(required=True), 'category': fields.Str(required=True), 'ceremony_id': fields.Str(required=True)}, location='json')
def add_post_it(args):
    team_id = request.args.get('team_id')
    #ceremony_id = args.get('ceremony_id')
    if not team_id:
        return jsonify({"error": "team_id is required"}), 400
    #if not team_id or not ceremony_id:
    #    return jsonify({"error": "team_id and ceremony_id are required"}),
    if not is_editing_allowed(team_id):
        return jsonify({"error": "Editing is not allowed at this time."}), 403
    #if not is_editing_allowed(team_id, ceremony_id):
    #    return jsonify({"error": "Editing is not allowed at this time."}), 403
    content = args.get('content')
    category = args.get('category')

    if not content or not category:
        return jsonify({"error": "Content and category are required"}), 400

    new_post_it = PostIt(content=content, team_id=team_id, category=category)
    #new_post_it = PostIt(content=content, team_id=team_id, category=category, ceremony_id=ceremony_id)
    try:
        post_it_dict = new_post_it.to_dict()
        result = mongo.db.post_its.insert_one(post_it_dict)
        post_it_dict['_id'] = str(result.inserted_id)
        
        return jsonify(post_it_dict), 201
    except Exception as e:
        error_message = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error: {error_message}")
        print(f"Traceback: {traceback_str}")
        return jsonify({"error": error_message}), 500

@post_its.route("/<post_it_id>", methods=['PUT'])
@use_args({'content': fields.Str(required=True), 'category': fields.Str(required=True)}, location='json')
#@use_args({'content': fields.Str(required=True), 'category': fields.Str(required=True), 'ceremony_id': fields.Str(required=True)}, location='json')
def update_post_it(args, post_it_id):
    team_id = request.args.get('team_id')
    #ceremony_id = args.get('ceremony_id')
    if not is_editing_allowed(team_id):
        return jsonify({"error": "Editing is not allowed at this time."}), 403
    #if not is_editing_allowed(team_id, ceremony_id):
    #    return jsonify({"error": "Editing is not allowed at this time."}), 403

    content = args.get('content')
    category = args.get('category')

    if not ObjectId.is_valid(post_it_id):
        return jsonify({"error": "Invalid post_it_id"}), 400

    if not content or not category:
        return jsonify({"error": "Content and category are required"}), 400

    try:
        result = mongo.db.post_its.update_one(
            {"_id": ObjectId(post_it_id), "team_id": team_id},
            #{"_id": ObjectId(post_it_id), "team_id": team_id, "ceremony_id": ceremony_id},
            {"$set": {"content": content, "category": category}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Post-It not found"}), 404
        
        updated_post_it = mongo.db.post_its.find_one({"_id": ObjectId(post_it_id)})
        if updated_post_it:
            updated_post_it['_id'] = str(updated_post_it['_id']) 
        
        return jsonify(updated_post_it), 200
    except Exception as e:
        
        print(f"Error updating post-it: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500

@post_its.route("/<post_it_id>", methods=['DELETE'])
def delete_post_it(post_it_id):
    team_id = request.args.get('team_id')
    #ceremony_id = request.args.get('ceremony_id')
    if not is_editing_allowed(team_id):
        return jsonify({"error": "Editing is not allowed at this time."}), 403
    #if not is_editing_allowed(team_id, ceremony_id):
    #    return jsonify({"error": "Editing is not allowed at this time."}), 403

    #try:
    #    if not team_id or not ceremony_id:
    #        return jsonify({"error": "team_id and ceremony_id are required"}), 400
    try:
        if not team_id:
            return jsonify({"error": "team_id is required"}), 400
        
        if not ObjectId.is_valid(post_it_id):
            return jsonify({"error": "Invalid post_it_id"}), 400
        
        result = mongo.db.post_its.delete_one({"_id": ObjectId(post_it_id), "team_id": team_id})
        #result = mongo.db.post_its.delete_one({"_id": ObjectId(post_it_id), "team_id": team_id, "ceremony_id": ceremony_id})
        if result.deleted_count == 0:
            return jsonify({"error": "Post-It not found"}), 404
        
        return jsonify({"message": "Post-It deleted successfully"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500