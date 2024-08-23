from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from app.models.post_it import PostIt
from app.db_connection import mongo
from app.routes.utils import validate_user_is_member_of_team  
from bson import ObjectId

post_its = Blueprint("post_its", __name__)


excluded_routes = []

@post_its.before_request
def apply_validate_user_is_member_of_team():
    if any(request.path.startswith(route) for route in excluded_routes):
        return None
    return validate_user_is_member_of_team()

@post_its.route("/", methods=['GET'])
@use_args({'team_id': fields.Str(required=True)}, location='query')
def get_post_its(args):
    team_id = args.get('team_id')


    if not team_id:
        return jsonify({"error": "team_id is required"}), 400


    post_its_cursor = mongo.db.post_its.find({"team_id": team_id})
    post_its = list(post_its_cursor)


    for post_it in post_its:
        post_it['_id'] = str(post_it['_id'])

    return jsonify(post_its)

@post_its.route("/", methods=['POST'])
@use_args({'content': fields.Str(required=True), 'category': fields.Str(required=True)}, location='json')
def add_post_it(args):
    content = args.get('content')
    category = args.get('category')
    team_id = request.args.get('team_id') 


    if not content or not category or not team_id:
        return jsonify({"error": "Content, category, and team_id are required"}), 400

    new_post_it = PostIt(content=content, team_id=team_id, category=category)

    try:
        post_it_dict = new_post_it.to_dict()
        result = mongo.db.post_its.insert_one(post_it_dict)
        post_it_dict['_id'] = str(result.inserted_id)
        return jsonify(post_it_dict), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@post_its.route("/<post_it_id>", methods=['PUT'])
@use_args({'content': fields.Str(required=True), 'category': fields.Str(required=True)}, location='json')
def update_post_it(args, post_it_id):
    content = args.get('content')
    category = args.get('category')
    team_id = request.args.get('team_id')
    if not team_id:
        return jsonify({"errors": ["Missing team_id in query parameters"]}), 422

    if not ObjectId.is_valid(post_it_id):
        return jsonify({"error": "Invalid post_it_id"}), 400

    # Validación de datos
    if not content or not category:
        return jsonify({"error": "Content and category are required"}), 400

    try:
        result = mongo.db.post_its.update_one(
            {"_id": ObjectId(post_it_id)},
            {"$set": {"content": content, "category": category}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Post-It not found"}), 404
        
        return jsonify({"message": "Post-It updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@post_its.route("/<post_it_id>", methods=['DELETE'])
def delete_post_it(post_it_id):
    try:

        if not ObjectId.is_valid(post_it_id):
            return jsonify({"error": "Invalid post_it_id"}), 400
        

        result = mongo.db.post_its.delete_one({"_id": ObjectId(post_it_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Post-It not found"}), 404
        
        return jsonify({"message": "Post-It deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500