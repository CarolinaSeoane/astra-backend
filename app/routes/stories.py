from datetime import datetime
import random
from flask import Blueprint, g, request, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from bson import ObjectId

from app.models.ceremony import Ceremony
from app.models.team import Team
from app.models.sprint import Sprint
from app.models.epic import Epic
from app.models.task import Task
from app.models.user import User
from app.models.story import Story
from app.models.configurations import Priority, Type, Configurations, Status
from app.models.notification import Notification
from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.services.notifications_services import notify_story_update


stories = Blueprint("stories", __name__)

excluded_routes = ["/stories/fields"]

DOING = Status.DOING.value
ALL_STORY_FIELDS = [
    "title",
    "description",
    "acceptance_criteria",
    "priority",
    "story_type",
    "assigned_to",
    "epic",
    "sprint",
    "estimation",
    # "estimation_method",
    "tasks",
]
EPIC_FIELD = "epic"
SPRINT_FIELD = "sprint"
TASKS_FIELD = "tasks"


@stories.before_request
def apply_validate_user_is_active_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_active_member_of_team()

@stories.route("/<view_type>", methods=["GET"])
@use_args(
    {
        "sprint": fields.Str(required=False),
        "assigned_to": fields.Str(required=False),
        "epic": fields.Str(required=False),
        "priority": fields.Str(required=False),
        "story_type": fields.Str(required=False),
        "story_id": fields.Str(required=False),
    },
    location="query",
)
def stories_list(args, view_type):
    team_stories = Story.get_stories_by_team_id(g.team_id, view_type, **args)
    return send_response(team_stories, [], 200, **g.req_data)

@stories.route("/fields", methods=["GET"])
@use_args({"sections": fields.Boolean(required=False, missing=False)}, location="query")
def story_fields(args):
    all_fields = Story.get_story_fields(args["sections"])
    return send_response(all_fields, [], 200, **g.req_data)

@stories.route("/filters", methods=["GET"])
@use_args(
    {
        ## available filters
        "sprints": fields.Boolean(required=False, missing=True),
        "members": fields.Boolean(required=False, missing=True),
        "epics": fields.Boolean(required=False, missing=True),
        "priority": fields.Boolean(required=False, missing=True),
        "story_type": fields.Boolean(required=False, missing=True),
        "estimation": fields.Boolean(required=False, missing=True),
        "task_statuses": fields.Boolean(required=False, missing=True),
        ## customization
        'year': fields.Integer(required=False), # affects sprints (TODO: should affect epics too!!!!)
        "future": fields.Boolean(
            required=False, missing=False
        ),  # affects sprints (TODO: should affect epics too!!!!)
        "backlog": fields.Boolean(
            required=False, missing=True
        ),
        "all_from_year": fields.Boolean(
            required=False, missing=False
        ),
    },
    location="query",
)
def filters(args):
    sprints_filter = []
    members_filter = []
    epics_filter = []
    priority = []
    story_type = []
    estimation = []
    task_statuses = []
    filters = {}
    team = []

    if args["sprints"]:
        sprints = Sprint.get_sprints(
            g.team_id, args.get('year'), args["future"], args["backlog"], args["all_from_year"]
        )

        if sprints:
            for sprint in sprints:
                sprint_option = {
                    "key": sprint["_id"]["$oid"],
                    "label": sprint["name"],
                    "status": sprint["status"],
                }
                sprints_filter.append(sprint_option)

        filters["sprint"] = {
            "label": "Sprint",
            "value": "sprint",
            "options": sprints_filter,
        }

    if args["members"] or args["epics"]:
        team = Team.get_team(g.team_id)

    if args["members"]:
        members = team.get("members")
        if members:
            for member in members:
                member_option = {
                    "key": member["_id"]["$oid"],
                    "label": member["username"]
                    + (" (You)" if member["_id"]["$oid"] == g._id else ""),
                    "username": member["username"],
                    "profile_picture": member["profile_picture"],
                    "email": member["email"],
                }
                members_filter.append(member_option)

        filters["assigned_to"] = {
            "label": "Assigned to",
            "value": "assigned_to",
            "options": members_filter,
        }

    if args["epics"]:
        if team.get("organization"):
            org_id = team["organization"]["$oid"]
            epics = Epic.get_epics_from_organization(org_id)
        else:
            epics = Epic.get_epics_from_team(g.team_id)

        if epics:
            for epic in epics:
                epic_option = {
                    'key': epic['_id']['$oid'],
                    'label': epic['title'],
                    'team': epic['team'],
                    'epic_color': epic['epic_color']
                }
                epics_filter.append(epic_option)

        filters["epic"] = {"label": "Epic", "value": "epic", "options": epics_filter}

    if args["priority"]:
        priority = [
            {"key": priority.value, "label": priority.value} for priority in Priority
        ]
        filters["priority"] = {
            "label": "Priority",
            "value": "priority",
            "options": priority,
        }

    if args["story_type"]:
        story_type = [{"key": _type.value, "label": _type.value} for _type in Type]
        filters["story_type"] = {
            "label": "Story type",
            "value": "story_type",
            "options": story_type,
        }

    if args["estimation"]:
        estimation_methods = team.get("estimation_method")
        try:
            estimation_methods.remove("planning_poker")
        except Exception:
            pass

        est_method = estimation_methods[0]
        estimation = Configurations.get_estimation_method_options(est_method)

        filters["estimation"] = {
            "label": estimation[est_method]["label"],
            "value": "estimation",
            "options": estimation[est_method]["options"],
        }

    if args["task_statuses"]:
        statuses = Task.get_statuses()
        for status in statuses:
            task_statuses.append({"label": status, "key": status})
        filters["task_statuses"] = task_statuses

    return send_response(filters, [], 200, **g.req_data)

@stories.route("/generate_id", methods=["GET"])
def generate_story_id():
    def generate_new_id():
        number = random.randint(1, 999999)
        complete_number = str(number).rjust(6, "0")
        team_name = Team.get_team(g.team_id)["name"].replace(" ", "_").upper()
        return team_name + "-" + complete_number

    story_id = generate_new_id()
    while Story.is_story_id_taken(story_id):
        story_id = generate_new_id()

    return send_response([story_id], [], 200, **g.req_data)

@stories.route("/create", methods=["POST"])
def create_story():
    story = request.json
    story["team"] = g.team_id

    tasks = Task.format(story)
    story["tasks"] = tasks
    story["subscribers"] = []
    story['story_status'] = Status.NOT_STARTED.value
    story["creation_date"] = datetime.combine(datetime.now().date(), datetime.min.time())

    resp = Story.create_story(story)
    Notification.create_assigned_notification(story, g.team_id)
    Notification.create_creator_notification(story, g.team_id)
    return send_response(
        [resp.get("message", [])], resp.get("error", []), resp["status"], **g.req_data
    )

@stories.route("/view", methods=["GET"])
@use_args({"story_id": fields.Str(required=True)}, location="query")
def retrieve_story(args):
    story = Story.get_story_by_id(args["story_id"])
    return send_response(story, [], 200, **g.req_data)

@stories.route("/edit", methods=["PUT"])
def edit_story():
    # if the story goes into doing, we need to include a start_date
    # if the story goes into done, we need to include an end_date
    # if the sprint is modified, we need to update the added_to_sprint value
    story = request.json
    story["team"] = g.team_id

    date_now = datetime.combine(datetime.now().date(), datetime.min.time())
    old_story = Story.get_story_by_id(story["story_id"])
    if not old_story:
        return send_response([], ["Old story not found"], 404, **g.req_data)

    if "_id" in story:
        del story["_id"]
    # story["estimation_method"] = old_story["estimation_method"]  # cannot be changed

    tasks = Task.format(story)
    story["tasks"] = tasks

    updated_fields = {}
    for field in ALL_STORY_FIELDS:
        if field == EPIC_FIELD:
            if old_story.get(field, {}).get("title") != story.get(field, {}).get("title"):
                updated_fields[field] = story.get(field)
        elif field == SPRINT_FIELD:
            if old_story.get(field, {}).get("name") != story.get(field, {}).get("name"):
                story["added_to_sprint"] = date_now
                updated_fields[field] = story.get(field)
        elif field == TASKS_FIELD:
            if Task.have_tasks_changed(old_story.get("tasks"), story["tasks"]):
                updated_fields[field] = story[field]
        elif old_story.get(field) != story.get(field):
            print(f"marking field {field} as updated")
            print(f"the old value was: {old_story.get(field)}")
            print(f"the new value is: {story.get(field)}")
            print("\n")
            updated_fields[field] = story.get(field)

    story["subscribers"] = old_story.get(
        "subscribers", []
    )  # new subscribers are handled by a different endpoint

    story_status = Task.get_story_status(story["tasks"])
    if story_status == DOING and "start_date" not in story:
        story["start_date"] = date_now
        updated_fields["start_date"] = story["start_date"]

    if updated_fields:
        print(f"actualizando story con updated fields: {updated_fields}")
        notify_story_update(old_story, updated_fields, g.team_id)

    if Story.is_done(story):
        resp = Story.finalize_story(story, g.team_id)
        print("Finalizando historia:", resp)
        return send_response(
            resp.get("message", []), resp.get("error", []), resp["status"], **g.req_data
        )

    story_status = Task.get_story_status(story["tasks"])
    if story_status == DOING and "start_date" not in story:
        story["start_date"] = date_now
        print(f"Start date added: {date_now}")

    resp = Story.update(story, story_status)
    user = User.get_user_by({"_id": ObjectId(g._id)})
    Story.save_modified_story(
        story_id=story["story_id"],
        title=story["title"],
        username=user.get("username", "Unknown"),
        modified_at=date_now,
        sprint=story["sprint"]["name"],
        team_id=story['team'],
    )
    return send_response(
        resp.get("message", []), resp.get("error", []), resp["status"], **g.req_data
    )

@stories.route("/subscribe/<story_id>", methods=["POST"])
def subscribe_to_story(story_id):
    resp = Story.subscribe_to_story(story_id, g._id)
    return send_response(
        resp["message"], resp.get("error", []), resp["status"], **g.req_data
    )

@stories.route("/unsubscribe/<story_id>", methods=["POST"])
def unsubscribe_to_story(story_id):
    resp = Story.unsubscribe_to_story(story_id, g._id)
    return send_response(
        resp["message"], resp.get("error", []), resp["status"], **g.req_data
    )

@stories.route('/modified_stories', methods=['GET'])
@use_args(
    {
        "team_id": fields.Str(required=True),
        "sprint": fields.Str(required=True),
        "ceremony_id": fields.Str(required=True)
    },
    location="query"
)
def get_modified_stories(args):
    ceremony_date = Ceremony.get_ceremony_date(args["ceremony_id"])
    # ceremony_date = datetime.combine(datetime.now().date(), datetime.min.time()) # testing only
    # print(f"ceremony date is {ceremony_date}")
    if not ceremony_date:
        return jsonify({"error": "No upcoming ceremony found for the team"}), 404

    modified_stories = Story.get_modified_stories_up_to(
        ceremony_date, args["team_id"], args["sprint"]
    )
    print(f"Modified stories found: {modified_stories}")

    return jsonify(modified_stories)

@stories.route('/list_with_story_status', methods=['GET'])
@use_args({'team_id': fields.Str(required=True),
           'sprint_current': fields.Str(required=True),
           'sprint_selected': fields.Str(required=True)},
          location='query')
def list_with_story_status(args):
    try:
        stories_list = Story.get_list_stories_in_team_id_by_sprint_current_and_selected(
            args["team_id"], args["sprint_current"], args["sprint_selected"]
        )
        return send_response(stories_list, [], 200, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to retrieve backlog stories: {e}"], 200, **g.req_data)

@stories.route('/update_story_sprint', methods=['PUT'])
@use_args({
    'team_id': fields.Str(required=True),
    'story_id': fields.Str(required=True),
    'new_sprint_name': fields.Str(required=True)
    },
    location='query')
def put_list_with_new_story_status(args):
    try:
        result = Story.put_new_status_and_new_sprint_to_story(
            args["team_id"], args["story_id"], args["new_sprint_name"]
        )

        if result:
            return send_response(True, [], 200, **g.req_data)
        return send_response(False, [], 200, **g.req_data)
    except Exception as e:
        return send_response(False, [f"Failed to put story status: {e}"], 200, **g.req_data)

@stories.route('/delete', methods=['DELETE'])
@use_args({"story_id": fields.Str(required=True)}, location="query")
def delete_story(args):
    resp = Story.delete(g.team_id, args["story_id"])
    return send_response(
        resp.get("message"), resp.get("error", []), resp["status"], **g.req_data
    )
