from datetime import datetime, timedelta
from flask import Blueprint, g, request
from webargs.flaskparser import use_args
from webargs import fields
from bson import ObjectId

from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.sprint import Sprint
from app.models.team import Team
from app.models.configurations import SprintStatus
from app.models.story import Story
from app.models.configurations import Status
from app.models.ceremony import Ceremony
from app.services.astra_scheduler import (
    get_weekday_number,
    generate_sprints_for_quarter,
    get_quarter
)


sprints = Blueprint('sprints', __name__)

excluded_routes = []

@sprints.before_request
def apply_validate_user_is_active_member_of_team():
    for excluded_route in excluded_routes:
        if (
            request.path.startswith(excluded_route['route'])
            and (request.method in excluded_route['methods'])
        ):
            return None

    return validate_user_is_active_member_of_team()

@sprints.route('/velocity/<sprint_name>', methods=['GET'])
def get_velocity(sprint_name):
    all_time_velocity = Sprint.get_velocity(g.team_id, sprint_name)
    velocity = all_time_velocity[-9:]
    return send_response(velocity, [], 200, **g.req_data)

@sprints.route('/burn_down_chart', methods=['GET'])
@use_args({"sprint_id": fields.Str(required=True)}, location="query")
def calculate_burn_down(args):
    sprint_name = args["sprint_id"]
    sprint_data = Sprint.get_start_and_end_dates(sprint_name, g.team_id)
    if not sprint_data:
        return send_response([], [], 200, **g.req_data)
    start_date = datetime.fromisoformat(sprint_data["start_date"]["$date"][:-1])
    end_date = datetime.fromisoformat(sprint_data["end_date"]["$date"][:-1])
    target = Sprint.get_target_points(sprint_name, g.team_id)

    current_date = start_date
    burn_down_data = {
        "target": target,
        "data": []
    }
    while current_date <= end_date:
        # target = Sprint.get_commited_points_up_to(
        #     sprint_name, g.team_id, current_date
        # )
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

@sprints.route('/all', methods=['GET'])
def get_sprints():
    all_sprints = Sprint.get_all_sprints(g.team_id)
    return send_response(all_sprints, [], 200, **g.req_data)

@sprints.route('/finish/attempt/<sprint_id>', methods=['PUT'])
def attempt_to_finish_sprint(sprint_id):
    # Validations before closing a sprint

    # Sprint can only be closed if its status is CURRENT
    sprint = Sprint.get_sprint_by({'_id': ObjectId(sprint_id)})

    if not sprint:
        return send_response([], ["Invalid sprint id."], 404, **g.req_data)

    if not sprint['status'] == SprintStatus.CURRENT.value:
        return send_response([], ["This sprint can't be closed."], 406, **g.req_data)

    # User must be SM of the team
    team_id = sprint['team']['$oid']

    if not Team.is_user_SM_of_team(g._id, team_id):
        return send_response(
            [], ["Forbidden. User is not authorized to access this resource"], 403, **g.req_data
        )

    # Actions

    # Notify stories still open
    open_stories = Story.get_stories_by_team_id(
        ObjectId(team_id),
        'list',
        story_status={'$ne': Status.DONE.value}, sprint=sprint['name']
    )

    # Notify day of closing
    end_date = datetime.fromisoformat(sprint["end_date"]["$date"][:-1])
    today = datetime.today()
    difference = (end_date - today).days
    # A positive number means the sprint is being closed BEFORE it's supposed to
    # A negative number means the sprint is being closed AFTER it was supposed to

    data = {
        # 'open_stories': None,
        'open_stories': open_stories,
        'date_diff': difference
    }
    return send_response(data, [], 200, **g.req_data)

@sprints.route('/finish/<sprint_id>', methods=['PUT'])
def finish_sprint(sprint_id):
    update_res = Sprint.finish_sprint(sprint_id)
    if update_res.modified_count == 1:
        return send_response([], [], 200, **g.req_data)
    return send_response([], ["Couldn't update sprint"], 404, **g.req_data)

@sprints.route('/start/<sprint_id>', methods=['PUT'])
def start_sprint(sprint_id):
    # Set new sprint as current
    update_res = Sprint.start_sprint(sprint_id)

    # Set following sprint as next
    Sprint.set_following_sprint(g.team_id)

    # Create and save ceremonies for current sprint
    Ceremony.create_sprint_ceremonies(g.team_id, sprint_id)

    if update_res.modified_count == 1:
        return send_response([], [], 200, **g.req_data)

    return send_response([], ["Couldn't update sprint"], 404, **g.req_data)

@sprints.route('', methods=["GET"])
@use_args({"sprint_name": fields.Str(required=True)}, location="query")
def get_sprint(args):
    filter = {
        "name": args["sprint_name"],
        "team": ObjectId(g.team_id)
    }
    sprint = Sprint.get_sprint_by(filter)
    return send_response(sprint, [], 200, **g.req_data)

@sprints.route('/create/attempt', methods=['GET'])
def attempt_to_create_sprint():
    # Get sprint setup
    sprint_begins_on = Team.get_team_settings(
        g.team_id, 'sprint_set_up'
    )['sprint_set_up']['sprint_begins_on']
    allowed_day = get_weekday_number(sprint_begins_on)

    # Get team's latest sprint
    latest_sprint = Sprint.get_latest_sprint(g.team_id)
    latest_end_date = latest_sprint['end_date'] if latest_sprint else datetime.today()

    # Return the possible start dates as a response
    return send_response(
        {'allowed_day': allowed_day, 'latest_sprint': latest_end_date}, [], 200, **g.req_data
    )

@sprints.route('/create', methods=['POST'])
@use_args({'start_date': fields.DateTime(required=True, format="iso")}, location='json')
def create_sprints(args):
    sprint_duration = Team.get_team_settings(
        g.team_id, 'sprint_set_up'
    )['sprint_set_up']['sprint_duration']
    latest_sprint = Sprint.get_latest_sprint(g.team_id)
    if not latest_sprint:
        latest_sprint_number = 0
    else:
        latest_sprint_number = (latest_sprint['sprint_number']
                            if latest_sprint['quarter'] == get_quarter(args['start_date'])
                            else 0)
    sprints = generate_sprints_for_quarter(args['start_date'], sprint_duration, g.team_id, latest_sprint_number)
    Sprint.add_sprints(sprints)

    there_is_a_next_sprint = Sprint.there_is_a_next_sprint(g.team_id)
    if not there_is_a_next_sprint:
        Sprint.set_following_sprint(g.team_id)

    # ToDo: handle errors
    return send_response([], [], 200, **g.req_data)

@sprints.route('/stories_status_rundown', methods=['GET'])
@use_args({"sprint_name": fields.Str(required=True)}, location='query')
def get_stories_status_rundown(args):
    results = Sprint.get_stories_grouped_by_status(args['sprint_name'], g.team_id)
    stories_by_status = []
    for res in results:
        res['name'] = res.pop('_id')
        stories_by_status.append(res)
    order = ["Not Started", "Doing", "Blocked", "Done"]
    data_dict = {item['name']: item['value'] for item in stories_by_status}
    stories_by_status_sorted = [{'name': name, 'value': data_dict.get(name, 0)} for name in order]
    # stories_by_status_sorted = sorted(stories_by_status, key=lambda x: order.index(x["name"]))
    return send_response(stories_by_status_sorted, [], 200, **g.req_data)

@sprints.route('/total_stories', methods=['GET'])
@use_args({"sprint_name": fields.Str(required=True)}, location='query')
def get_total_stories(args):
    total_count = Sprint.get_total_stories_count(args["sprint_name"], g.team_id)
    return send_response(total_count, [], 200, **g.req_data)

@sprints.route('/future_and_current', methods=['GET'])
@use_args({"team_id": fields.Str(required=True)}, location='query')
def get_future_and_current_sprints(args):
    documents = Sprint.get_future_sprints(args["team_id"])
    return send_response(documents, [], 200, **g.req_data)

@sprints.route('/current', methods=['GET'])
@use_args({"team_id": fields.Str(required=True)}, location='query')
def get_current_sprint(args):
    documents = Sprint.get_current_sprint(args["team_id"])
    return send_response(documents, [], 200, **g.req_data)
