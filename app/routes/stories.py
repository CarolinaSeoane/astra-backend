import random
from datetime import datetime, timedelta
from flask import Blueprint, g, request,jsonify
from webargs.flaskparser import use_args
from webargs import fields
from bson import ObjectId
from dateutil import parser

from app.models.story import Story
from app.utils import get_current_quarter, send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.team import Team
from app.models.sprint import Sprint
from app.models.epic import Epic
from app.models.task import Task
from app.models.user import User
from app.models.ceremony import Ceremony
from app.services.mongoHelper import MongoHelper
from app.models.configurations import Priority, Type, Configurations, Status
from app.models.notification import Notification
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

@stories.route("/standup/<view_type>", methods=['GET'])
@use_args({
    'sprint': fields.Str(required=False),
    'assigned_to': fields.Str(required=False),
    'epic': fields.Str(required=False),
    'priority': fields.Str(required=False),
    'story_type': fields.Str(required=False),
    'story_id': fields.Str(required=False),
    'ceremony_id': fields.Str(required=False)  
}, location='query')
def standup_stories_list(args, view_type):
    ceremony_date = None
    if 'ceremony_id' in args and args['ceremony_id']:
        ceremony_date = get_ceremony_date(args['ceremony_id'])
        print("Ceremony ID:", args['ceremony_id'])
        print("Fecha de ceremonia obtenida:", ceremony_date)
        if ceremony_date is None:
            return send_response(
                [], ["No se pudo obtener la fecha de la ceremonia."], 400, **g.req_data
            )
    stories = Story.get_standup_stories(g.team_id, view_type,ceremony_date=ceremony_date, **args)
    print("Lista de historias obtenidas:",stories)
    return send_response(stories, [], 200, **g.req_data)

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
        "quarter": fields.Str(
            required=False, missing=str(get_current_quarter(datetime.today()))
        ),  # affects sprints (TODO: should affect epics too!!!!)
        "year": fields.Str(
            required=False, missing=str(datetime.today().year)
        ),  # affects sprints (TODO: should affect epics too!!!!)
        "future": fields.Str(
            required=False, missing=False
        ),  # affects sprints (TODO: should affect epics too!!!!)
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
            g.team_id, args["quarter"], args["year"], args["future"]
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
                    "key": epic["_id"]["$oid"],
                    "label": epic["title"],
                    "team": epic["team"],
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

    nueva_fecha = parser.isoparse(old_story["creation_date"]['$date'])
    fecha_normalizada = datetime.combine(nueva_fecha.date(), datetime.min.time())
    print(f"fecha cracion: {fecha_normalizada}")
    print(f"Received story for editing: {old_story}")
    user = get_current_user()
    username = user["username"]
    modified_story_info = {
        "story_id": story["story_id"],
        "title": story["title"],
        "modified_by": username,
        "modified_at": date_now, 
        "sprint": story["sprint"]["name"],
        "team_id":story['team']
    }

    if "_id" in story:
        del story["_id"]
    # story["estimation_method"] = old_story["estimation_method"]  # cannot be changed
    if "creation_date" in old_story:
        story["creation_date"] = fecha_normalizada

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
    save_modified_story(
        modified_story_info["story_id"],
        modified_story_info["title"],
        modified_story_info["modified_by"],
        modified_story_info["modified_at"],
        modified_story_info["sprint"],
        modified_story_info["team_id"],
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
def get_modified_stories():
    mongo_helper = MongoHelper()
    team_id = request.args.get('team_id')
    sprint_id = request.args.get('sprint')
    ceremony_id = request.args.get('ceremony_id')

    print(f"Received team_id: {team_id}, sprint: {sprint_id}, ceremony_id: {ceremony_id}")

    ceremony_date = get_ceremony_date(ceremony_id)
    if not ceremony_date:
        return jsonify({"error": "No upcoming ceremony found for the team"}), 404
    print("fecha2",ceremony_date)
    filter_query = {
        'team_id': ObjectId(team_id),
        'modified_at': {'$lt': ceremony_date}
        }

    if sprint_id:
        filter_query['sprint'] = sprint_id

    modified_stories = mongo_helper.get_documents_by('modified_stories', filter_query)
    print(f"Filter query: {filter_query}")
    print(f"Modified stories found: {modified_stories}")

    return jsonify(modified_stories)

def save_modified_story(story_id, title, username, modified_at,sprint,team_id):
    mongo_helper = MongoHelper()
    modified_story = {
        "story_id": story_id,
        "title": title,
        "username": username,
        "modified_at": modified_at,
        "sprint": sprint,
        "team_id": team_id
    }
    print(f"Saving modified story: {modified_story}")
    result = mongo_helper.create_document('modified_stories', modified_story)
    print(f"Result of save: {result}")

def get_current_user():
    user_id = g._id
    if user_id:
        user = User.get_user_by({"_id": ObjectId(user_id)})
        return user
    return None

def get_ceremony_date(ceremony_id):
    """Obtiene la fecha de la ceremonia especificada por su ID y retorna el día anterior."""
    ceremony = Ceremony.get_ceremony_by_id(ceremony_id)

    print(f"Ceremony data: {ceremony}")
    if not ceremony:
        print("Error: No se encontró la ceremonia con el ID proporcionado.")
        return None

    if 'ends' not in ceremony or not ceremony['ends']:
        print("Error: No se encontró la fecha de fin ('ends') en la ceremonia.")
        return None

    if isinstance(ceremony['ends'], dict) and '$date' in ceremony['ends']:
        ends_date_str = ceremony['ends']['$date']
        ceremony_date = datetime.fromisoformat(ends_date_str[:-1]) - timedelta(days=1)
        print(f"Using ceremony date for filtering: {ceremony_date}")
        return ceremony_date
    else:
        print("Error: 'ends' no es un dict o no contiene '$date'.")
        return None

@stories.route('/list_with_story_status', methods=['GET'])
@use_args({'team_id': fields.Str(required=True),
           'sprint_current': fields.Str(required=True),
           'sprint_selected': fields.Str(required=True)},
          location='query')
def list_with_story_status(args):
    team_id = args.get('team_id')
    sprint_current =  args.get('sprint_current')
    sprint_selected =  args.get('sprint_selected')

    #print("    team_id",team_id )
    #print("    sprint ", sprint)
    #team_id = args['team_id']  # Extraer team_id de los argumentos
    #sprint = args['sprint']
    try:
        stories = Story.get_list_stories_in_team_id_by_sprint_current_and_selected(
            team_id, sprint_current, sprint_selected
        )  # Llamar a la función mejorada
        #print("stories", stories)
        return send_response(stories, [], 200, **g.req_data)  # Retornar historias
    except Exception as e:
        #print(f"Error retrieving backlog stories: {e}")
        return send_response([], [f"Failed to retrieve backlog stories: {e}"], 200, **g.req_data)

@stories.route('/update_story_sprint', methods=['PUT'])
@use_args({
    'team_id': fields.Str(required=True),
    'story_id': fields.Str(required=True),
    'new_sprint_name': fields.Str(required=True)
    },
    location='query')
def put_list_with_new_story_status(args):
    team_id = args.get('team_id')
    story_id = args.get('story_id')
    new_sprint_name = args.get('new_sprint_name')

    #print("team_id:", team_id)
    #print("story_id:", story_id)
    #print("new_sprint_name", new_sprint_name)

    #if(new_status=="Backlog")
    #{new_status=="Not Started"}

    try:
        result = Story.put_new_status_and_new_sprint_to_story(
            team_id, story_id, new_sprint_name
        ) #Move between sprints

        if result:  # Verificar si result es verdadero (true)
            return send_response(True, [], 200, **g.req_data)  # Retornar éxito
        return send_response(False, [], 200, **g.req_data)  # Retornar fallo
    except Exception as e:
        return send_response(False, [f"Failed to put story status: {e}"], 200, **g.req_data)

@stories.route('/delete', methods=['DELETE'])
@use_args({"story_id": fields.Str(required=True)}, location="query")
def delete_story(args):
    resp = Story.delete(g.team_id, args["story_id"])
    MongoHelper().delete_many("modified_stories", {
        "team_id": g.team_id,
        "story_id": args["story_id"]
    })
    return send_response(
        resp.get("message"), resp.get("error", []), resp["status"], **g.req_data
    )
