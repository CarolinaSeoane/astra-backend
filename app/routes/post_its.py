from datetime import datetime, timedelta
import traceback
from bson import ObjectId
from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
from webargs import fields

from app.models.post_it import PostIt
from app.models.ceremony import Ceremony
from app.routes.utils import validate_user_is_active_member_of_team

post_its = Blueprint("post_its", __name__)

excluded_routes = []

content_category_args = {
    'content': fields.Str(required=True),
    'category': fields.Str(required=True)
}

team_id_ceremony_id_args = {
    'team_id': fields.Str(required=True),
    'ceremony_id': fields.Str(required=True)
}

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
@use_args(team_id_ceremony_id_args, location='query')
def get_post_its(args):
    ceremony_post_its = PostIt.get_post_its(args["team_id"], args["ceremony_id"])
    return jsonify(ceremony_post_its)

@post_its.route("/", methods=['POST'])
@use_args(content_category_args, location='json')
@use_args(team_id_ceremony_id_args, location='query')
def add_post_it(json_args, query_args):
    new_post_it = PostIt(
        content=json_args["content"],
        team_id=query_args["team_id"],
        category=json_args["category"],
        ceremony_id=query_args["ceremony_id"]
    )

    try:
        post_it_dict = PostIt.create_post_it(new_post_it)
        return jsonify(post_it_dict), 201
    except Exception as e:
        error_message = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error: {error_message}")
        print(f"Traceback: {traceback_str}")
        return jsonify({"error": error_message}), 500

@post_its.route("/<post_it_id>", methods=['PUT'])
@use_args(content_category_args, location='json')
@use_args(team_id_ceremony_id_args, location='query')
def update_post_it(json_args, query_args, post_it_id):
    if not ObjectId.is_valid(post_it_id):
        return jsonify({"error": "Invalid post_it_id"}), 400

    new_post_it = PostIt(
        content=json_args["content"],
        team_id=query_args["team_id"],
        category=json_args["category"],
        ceremony_id=query_args["ceremony_id"]
    )
    try:
        updated_post_it = PostIt.update_post_it(new_post_it, post_it_id)
        if not update_post_it:
            return jsonify({"error": "Post-It not found"}), 404
        return jsonify(updated_post_it), 200
    except Exception as e:
        print(f"Error updating post-it: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500

@post_its.route("/<post_it_id>", methods=['DELETE'])
@use_args(team_id_ceremony_id_args, location='query')
def delete_post_it(args, post_it_id):
    if not ObjectId.is_valid(post_it_id):
        return jsonify({"error": "Invalid post_it_id"}), 400

    try:
        result = PostIt.delete_post_it(post_it_id, args["team_id"], args["ceremony_id"])
        if not result:
            return jsonify({"error": "Post-It not found"}), 404
        return jsonify({"message": "Post-It deleted successfully"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
