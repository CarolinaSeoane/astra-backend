from datetime import datetime
from flask import Blueprint, g
from webargs.flaskparser import use_args
from webargs import fields

from app.models.story import Story
from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.sprint import Sprint

sprints = Blueprint('sprints', __name__)


@sprints.before_request
def apply_validate_user_is_active_member_of_team():
    return validate_user_is_active_member_of_team()

@sprints.route('/velocity', methods=['GET'])
def get_velocity():
    velocity = Sprint.get_velocity(g.team_id) # TODO trim down the response to x previous sprints
    return send_response(velocity, [], 200, **g.req_data)

@sprints.route('/burn_down_chart', methods=['GET'])
@use_args({"sprint_id": fields.Str(required=True)}, location="query")
def calculate_burn_down(args):
    target = Sprint.get_target_points(args["sprint_id"], g.team_id)
    stories = Story.get_done_story_points_count_by_day(args["sprint_id"], g.team_id)
    burn_down_data = []
    remainder = target
    for story in stories:
        remainder -= story["completed_points"]
        burn_down_data.append({
            "day": story["_id"].strftime("%a, %d"),
            "remaining": remainder
        }) # TODO completar gaps con el valor anterior y hacer que llegue hasta el ultimo dia actual
    return send_response(burn_down_data, [], 200, **g.req_data)
