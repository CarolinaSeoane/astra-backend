from flask import Blueprint, g

from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.sprint import Sprint


sprints = Blueprint('sprints', __name__)

@sprints.before_request
def apply_validate_user_is_active_member_of_team():
    return validate_user_is_active_member_of_team()

@sprints.route('/velocity', methods=['GET'])
def get_velocity():
    velocity = Sprint.get_velocity(g.team_id)
    return send_response(velocity, [], 200, **g.req_data)
