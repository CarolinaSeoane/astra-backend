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
    # get the sum of the story points that were closed (done) up to a certain date
    # we'll run a for loop starting on sprint start and finishing on sprint end

    # fetch sprint start and end date
    sprint_name = args["sprint_id"]
    sprint_data = Sprint.get_start_and_end_dates(sprint_name, g.team_id)
    start_date = datetime.fromisoformat(sprint_data["start_date"]["$date"][:-1])
    end_date = datetime.fromisoformat(sprint_data["end_date"]["$date"][:-1])
    original_target = Sprint.get_target_points(sprint_name, g.team_id)

    current_date = start_date
    burn_down_data = {
        "target": original_target,
        "data": []
    }
    while current_date <= end_date:
        target = Sprint.get_commited_points_up_to(
            sprint_name, g.team_id, current_date
        )
        completed_points_so_far = Sprint.get_completed_points_up_to(
            sprint_name, g.team_id, current_date
        )
        if not completed_points_so_far:
            remaining = target
        else:
            remaining = target - completed_points_so_far[0]["completed_points"]
        burn_down_data["data"].append({
            "day": current_date.strftime("%a, %d"),
            "remaining": remaining
        })
        print(f"for date {current_date}, the target is {target} and the completed points so far "
              f"are {completed_points_so_far}, hence, the remaining is {remaining}")
        current_date += timedelta(days=1)  # Move to the next day
        print("end of one loop")

    return send_response(burn_down_data, [], 200, **g.req_data)

    # for loop from start date to end date
    # mongo query for stories that are closed and whose closed date is less than or 
    # equal to current date of foor loop (from sprint)
    # check if value is none, complete with previous value (actually, this woudnt happen)
    # append result to data





    # sprint_data = Sprint.get_target_points_and_dates(args["sprint_id"], g.team_id)
    # stories = Story.get_done_story_points_count_by_day(args["sprint_id"], g.team_id)
    # burn_down_data = []
    # burn_down_chart = {
    #     "data": burn_down_data,
    #     "sprint_end": sprint_data["end_date"]
    # }
    # remainder = sprint_data["target"]
    # previous_day = datetime.strptime(sprint_data["start_date"]['$date'], '%Y-%m-%d')
    # print(previous_day)
    # date_now = datetime.now().strftime("%Y-%m-%d")
    # cumulative_difference = 0
    # for index, story in enumerate(stories):
    #     cumulative_difference += story["completed_points"]
        
    #     remainder -= story["completed_points"]
    #     day = story["_id"]
    #     if previous_day + timedelta(days=1) != day:
    #         burn_down_data.append({
    #             "day": previous_day + timedelta(days=1).strftime("%a, %d"),
    #             "remaining": stories[index - 1]["completed_points"]
    #         })
    #     previous_day = day
    #     burn_down_data.append({
    #         "day": day.strftime("%a, %d"),
    #         "remaining": remainder
    #     }) # TODO completar gaps con el valor anterior y hacer que llegue hasta el dia actual
    # return send_response(burn_down_chart, [], 200, **g.req_data)
