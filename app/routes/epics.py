from math import ceil
from flask import Blueprint, request, g
from webargs.flaskparser import use_args
from webargs import fields
from bson import ObjectId

from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.team import Team
from app.models.configurations import Status, Priority, Color
from app.models.epic import Epic


epics = Blueprint('epics', __name__)

excluded_routes = [
    '/epics/fields'
]

@epics.before_request
def apply_validate_user_is_active_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_active_member_of_team()

@epics.route('/create', methods=['POST'])
def create_story():
    epic = request.json
    epic['team'] = g.team_id
    org = Team.get_organization(g.team_id)
    epic['organization'] = ObjectId(org['$oid'])
    epic['status'] = Status.NOT_STARTED.value # revisar!!

    resp = Epic.create_epic(epic)
    return send_response(
        [resp.get("message", [])], resp.get("error", []), resp["status"], **g.req_data
    )

@epics.route("/fields", methods=['GET'])
@use_args({
    "sections": fields.Boolean(required=False, missing=False),
    "only_keys": fields.Boolean(required=False, missing=False)
    }, location='query')
def story_fields(args):
    if args['only_keys']:
        field_names = Epic.get_names_of_mandatory_fields()
    else:
        field_names = Epic.get_epic_fields(args["sections"])
    return send_response(field_names, [], 200, **g.req_data)

@epics.route("/filters", methods=['GET'])
@use_args({
    ## available filters
    'colors': fields.Boolean(required=False, missing=True),
    'priority': fields.Boolean(required=False, missing=True),
    ## customization
    # None
    }, location='query')
def filters(args):
    color = []
    priority = []
    filters = {}

    if args['colors']:
        color = [{'key': col.name, 'label': col.value} for col in Color]
        filters['epic_color'] = {
            'label': 'Color',
            'value': 'epic_color',
            'options': color
        }

    if args['priority']:
        priority = [{'key': priority.value, 'label': priority.value} for priority in Priority]
        filters['priority'] = {
            'label': 'Priority',
            'value': 'priority',
            'options': priority
        }

    return send_response(filters, [], 200, **g.req_data)

@epics.route("/get_epic_count_by_sprint", methods=['GET'])
@use_args({"sprint_name": fields.Str(required=True)}, location='query')
def get_epic_count_by_sprint(args):
    cursor = Epic.get_count_by_sprint(args['sprint_name'], g.team_id)
    cursor_list = list(cursor)
    results = []
    total = 0
    for doc in cursor_list:
        total += doc['count']

    for doc in cursor_list:
        per = ceil(doc['count'] * 100 / total)
        epic_info = {
            "name": doc['_id'],
            "value": doc['count'],
            "percentage": f"{per}%"
        }
        results.append(epic_info)
    return send_response(results, [], 200, **g.req_data)
