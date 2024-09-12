from flask import Blueprint, g, request

from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.services.google_meet import create_space

ceremonies = Blueprint("ceremonies", __name__)

excluded_routes = [
    '/ceremonies/event' # change
]

@ceremonies.before_request
def apply_validate_user_is_active_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_active_member_of_team()

@ceremonies.route("/event", methods=['GET'])
def create_google_meet_space():
    event = create_space()
    return send_response([event], [], 200, {'key': '**g.req_data'}, '')