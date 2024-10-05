from datetime import datetime, timedelta
from flask import Blueprint, g, request
from webargs.flaskparser import use_args
from webargs import fields
from bson import ObjectId, decode
from json import loads

from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.sprint import Sprint
from app.models.team import Team
from app.models.configurations import SprintStatus
from app.models.story import Story
from app.models.configurations import Status


sprints = Blueprint('sprints', __name__)

excluded_routes = [
    {
        'route': '/sprints/finish', # shouldnt be here
        'methods': ['PUT']
    },
    {
        'route': '/sprints/start', # shouldnt be here
        'methods': ['PUT']
    },
]

@sprints.before_request
def apply_validate_user_is_active_member_of_team():
    for excluded_route in excluded_routes:
        if request.path.startswith(excluded_route['route']) and (request.method in excluded_route['methods']):
            return None

    return validate_user_is_active_member_of_team()

@sprints.route('/velocity', methods=['GET'])
def get_velocity():
    velocity = Sprint.get_velocity(g.team_id) # TODO trim down the response to x previous sprints
    # TODO get velocity up to current date
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

@sprints.route('/all', methods=['GET'])
def get_sprints():
    sprints = Sprint.get_all_sprints(g.team_id)
    return send_response(sprints, [], 200, **g.req_data)

@sprints.route('/finish/attempt/<sprint_id>', methods=['PUT'])
def attempt_to_finish_sprint(sprint_id):
    # Validations before closing a sprint

    ## Sprint can only be closed if its status is CURRENT
    sprint = Sprint.get_sprint_by(ObjectId(sprint_id))

    if not sprint:
        return send_response([], ["Invalid sprint id."], 404, **g.req_data)

    if not sprint['status'] == SprintStatus.CURRENT.value:
        return send_response([], ["This sprint can't be closed."], 406, **g.req_data)

    ## User must be SM of the team
    team_id = sprint['team']['$oid']

    if not Team.is_user_SM_of_team(g._id, team_id):
        return send_response([], ["Forbidden. User is not authorized to access this resource"], 403, **g.req_data)
    
    # Actions
    
    ## Notify stories still open
    open_stories = Story.get_stories_by_team_id(ObjectId(team_id), 'list', story_status={'$ne': Status.DONE.value}, sprint=sprint['name'])
    
    ## Notify day of closing
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
    Sprint.set_following_sprint(sprint_id)
    
    # Create ceremonies for current sprint
    
    
    if update_res.modified_count == 1:
        return send_response([], [], 200, **g.req_data)

    return send_response([], ["Couldn't update sprint"], 404, **g.req_data)
