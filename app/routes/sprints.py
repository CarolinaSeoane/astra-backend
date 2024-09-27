from datetime import datetime, timedelta
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
    sprint_data = Sprint.get_target_points_and_dates(args["sprint_id"], g.team_id)
    stories = Story.get_done_story_points_count_by_day(args["sprint_id"], g.team_id)
    burn_down_data = []
    burn_down_chart = {
        "data": burn_down_data,
        "sprint_end": sprint_data["end_date"]
    }
    remainder = sprint_data["target"]
    previous_day = datetime.strptime(sprint_data["start_date"]['$date'], '%Y-%m-%d')
    print(previous_day)
    date_now = datetime.now().strftime("%Y-%m-%d")
    for index, story in enumerate(stories):
        remainder -= story["completed_points"]
        day = story["_id"]
        if previous_day + timedelta(days=1) != day:
            burn_down_data.append({
                "day": previous_day + timedelta(days=1).strftime("%a, %d"),
                "remaining": stories[index - 1]["completed_points"]
            })
        previous_day = day
        burn_down_data.append({
            "day": day.strftime("%a, %d"),
            "remaining": remainder
        }) # TODO completar gaps con el valor anterior y hacer que llegue hasta el dia actual
    return send_response(burn_down_chart, [], 200, **g.req_data)
