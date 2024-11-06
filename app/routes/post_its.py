from datetime import datetime, timedelta
import traceback
from bson import ObjectId
from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
from webargs import fields

from app.models.post_it import PostIt
from app.models.ceremony import Ceremony
from app.db_connection import mongo
from app.routes.utils import validate_user_is_active_member_of_team

post_its = Blueprint("post_its", __name__)

excluded_routes = []

@post_its.before_request
def apply_validate_user_is_active_member_of_team():
    if any(request.path.startswith(route) for route in excluded_routes):
        return None
    return validate_user_is_active_member_of_team()

def is_retroboard_active(team_id):
    ceremony = Ceremony.get_current_ceremony_by_team_id(team_id)
    if not ceremony:
        upcoming_ceremonies = Ceremony.get_upcoming_ceremonies_by_team_id(team_id)
        if upcoming_ceremonies:
            ceremony = upcoming_ceremonies[0]
        else:
            return False

    print(ceremony)

    if isinstance(ceremony, list):
        ceremony = ceremony[0]

    starts = ceremony.get('starts')
    ends = ceremony.get('ends')

    if isinstance(starts, dict) and '$date' in starts:
        starts = starts['$date']
    if isinstance(ends, dict) and '$date' in ends:
        ends = ends['$date']

    if isinstance(starts, str):
        starts = datetime.fromisoformat(starts)
    if isinstance(ends, str):
        ends = datetime.fromisoformat(ends)

    if starts.tzinfo is not None:
        starts = starts.replace(tzinfo=None)
    if ends.tzinfo is not None:
        ends = ends.replace(tzinfo=None)

    start_time_with_buffer = starts - timedelta(minutes=10)

    return start_time_with_buffer <= datetime.now() <= ends

@post_its.route("/", methods=['GET'])
@use_args(
    {'team_id': fields.Str(required=True), 'ceremony_id': fields.Str(required=True)},
    location='query'
)
def get_post_its(args):
    team_id = args.get('team_id')
    ceremony_id = args.get('ceremony_id')

    if not team_id or not ceremony_id:
        return jsonify({"error": "team_id and ceremony_id are required"}), 400

    post_its_cursor = mongo.db.post_its.find(
        {"team_id": team_id, "ceremony_id": ceremony_id}
    )
    post_its = list(post_its_cursor)

    for post_it in post_its:
        post_it['_id'] = str(post_it['_id'])

    return jsonify(post_its)

@post_its.route("/", methods=['POST'])
@use_args(
    {'content': fields.Str(required=True), 'category': fields.Str(required=True)},
    location='json'
)
def add_post_it(args):
    team_id = request.args.get('team_id')
    ceremony_id = request.args.get('ceremony_id')

    if not team_id or not ceremony_id:
        return jsonify({"error": "team_id and ceremony_id are required"}), 400

    if not is_retroboard_active(team_id):
        return jsonify({"error": "Post-its can only be created during the ceremony."}), 403

    content = args.get('content')
    category = args.get('category')

    if not content or not category:
        return jsonify({"error": "Content and category are required"}), 400

    new_post_it = PostIt(
        content=content,
        team_id=team_id,
        category=category,
        ceremony_id=ceremony_id
    )

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
@use_args(
    {'content': fields.Str(required=True), 'category': fields.Str(required=True)},
    location='json'
)
def update_post_it(args, post_it_id):
    team_id = request.args.get('team_id')
    ceremony_id = request.args.get('ceremony_id')

    if not team_id or not ceremony_id:
        return jsonify({"error": "team_id and ceremony_id are required"}), 400

    if not is_retroboard_active(team_id):
        return jsonify({"error": "Post-its can only be updated during the ceremony."}), 403

    content = args.get('content')
    category = args.get('category')

    if not ObjectId.is_valid(post_it_id):
        return jsonify({"error": "Invalid post_it_id"}), 400

    if not content or not category:
        return jsonify({"error": "Content and category are required"}), 400

    try:
        result = mongo.db.post_its.update_one(
            {"_id": ObjectId(post_it_id), "team_id": team_id, "ceremony_id": ceremony_id},
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
    ceremony_id = request.args.get('ceremony_id')

    if not team_id or not ceremony_id:
        return jsonify({"error": "team_id and ceremony_id are required"}), 400

    if not is_retroboard_active(team_id):
        return jsonify({"error": "Post-its can only be deleted during the ceremony."}), 403

    try:
        if not ObjectId.is_valid(post_it_id):
            return jsonify({"error": "Invalid post_it_id"}), 400

        result = mongo.db.post_its.delete_one(
            {"_id": ObjectId(post_it_id), "team_id": team_id, "ceremony_id": ceremony_id}
        )

        if result.deleted_count == 0:
            return jsonify({"error": "Post-It not found"}), 404

        return jsonify({"message": "Post-It deleted successfully"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@post_its.route("/save_board", methods=['POST'])
@use_args({'board_state': fields.Raw(required=True)}, location='json')
def save_board_state(args):
    team_id = request.args.get('team_id')
    ceremony_id = request.args.get('ceremony_id')

    if not team_id or not ceremony_id:
        return jsonify({"error": "team_id and ceremony_id are required"}), 400

    if not is_retroboard_active(team_id):
        return jsonify({"error": "Board state can only be saved after the ceremony."}), 403

    board_state = args.get('board_state')

    try:
        mongo.db.boards.insert_one({
            'team_id': team_id,
            'ceremony_id': ceremony_id,
            'board_state': board_state,
            'saved_at': datetime.utcnow()
        })
        return jsonify({"message": "Board state saved successfully."}), 201
    except Exception as e:
        error_message = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error: {error_message}")
        print(f"Traceback: {traceback_str}")
        return jsonify({"error": error_message}), 500
