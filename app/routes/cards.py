from flask import Blueprint, request, g, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from app.models.card import Card  
from app.db_connection import mongo
from app.routes.utils import validate_user_is_active_member_of_team
from bson import ObjectId
from app.models.ceremony import Ceremony
from app.models.sprint import Sprint
from datetime import datetime, timedelta
from app.utils import send_response

cards = Blueprint("cards", __name__)

excluded_routes = []

@cards.before_request
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

@cards.route("/total_stories", methods=['GET'])
@use_args({'sprint_name': fields.Str(required=True)}, location='query')
def get_total_stories(args):
    total_count = Sprint.get_total_stories_count(args["sprint_name"], g.team_id)
    return send_response(total_count, [], 200, **g.req_data)

@cards.route("/", methods=['GET'])
@use_args({'team_id': fields.Str(required=True), 'sprint_name': fields.Str(required=True)}, location='query')
def get_cards(args):
    team_id = args.get('team_id')
    sprint_name = args.get('sprint_name')

    if not team_id or not sprint_name:
        return jsonify({"error": "team_id and sprint_name are required"}), 400

    cards_cursor = mongo.db.cards.find({"team_id": team_id, "sprint_name": sprint_name})
    
    cards_list = list(cards_cursor)

    for card in cards_list:
        card['_id'] = str(card['_id'])

    return jsonify(cards_list)