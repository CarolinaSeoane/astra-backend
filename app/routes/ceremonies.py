from flask import Blueprint, request, g, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from bson import ObjectId

from app.utils import send_response, apply_banner_format
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.ceremony import Ceremony
from app.models.configurations import CeremonyType, CeremonyStatus, GoogleMeetDataStatus
from app.models.sprint import Sprint
from app.models.user import User


ceremonies = Blueprint("ceremonies", __name__)

excluded_routes = []

@ceremonies.before_request
def apply_validate_user_is_active_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_active_member_of_team()

@ceremonies.route('/banner', methods=['GET'])
def team_upcoming_ceremonies():
    upcoming_ceremonies = Ceremony.get_upcoming_ceremonies_by_team_id(g.team_id)
    banner_formatted_ceremonies = apply_banner_format(upcoming_ceremonies)
    return send_response(banner_formatted_ceremonies, [], 200, **g.req_data)

@ceremonies.route('', methods=['GET'])
@use_args({
    'sprint': fields.Str(required=False),
    'ceremony_type': fields.Str(required=False),
    'ceremony_status': fields.Str(required=False),
    }, location='query')
def ceremonies_list(args):
    team_ceremonies = Ceremony.get_ceremonies_by_team_id(g.team_id, **args)
    return send_response(team_ceremonies, [], 200, **g.req_data)

@ceremonies.route('/meet/data/<ceremony_id>', methods=['GET'])
def get_ceremonies_meet_data(ceremony_id):
    user_doc = User.get_user_by({'email': g.email}, True)
    user_obj = User(**user_doc)
    ceremony = Ceremony.get_ceremonies_by_team_id(g.team_id, ceremony_id=ObjectId(ceremony_id))[0]
    if not ceremony.get('attendees') or ceremony.get('attendees') == GoogleMeetDataStatus.UNAVAILABLE.value:
        ceremony_data = Ceremony.get_google_meet_data(user_obj, ceremony)
    else:
        ceremony_data = {'attendees': ceremony['attendees'], 'transcript': ceremony.get('transcript', GoogleMeetDataStatus.UNAVAILABLE.value)}
    return send_response(ceremony_data, [], 200, **g.req_data)

@ceremonies.route("/filters", methods=['GET'])
@use_args({
    ## available filters
    'sprints': fields.Boolean(required=False, missing=True),
    'ceremony_type': fields.Boolean(required=False, missing=True),
    'ceremony_status': fields.Boolean(required=False, missing=True),
    ## customization
    'year': fields.Integer(required=False),
    "future": fields.Boolean(required=False, missing=False),
    "backlog": fields.Boolean(required=False, missing=True),
    "all_from_year": fields.Boolean(required=False, missing=False),
    }, location='query')
def filters(args):
    sprints_filter = []
    ceremony_type = []
    ceremony_status = []
    filters = {}

    if args['sprints']:
        sprints = Sprint.get_sprints(g.team_id, args.get('year'), args['future'], args['backlog'])

        if sprints:
            for sprint in sprints:
                sprint_option = {
                    'key': sprint['_id']['$oid'],
                    'label': sprint['name'],
                    'status': sprint['status']
                }
                sprints_filter.append(sprint_option)

        filters['sprint'] = {
            'label': 'Sprint',
            'value': 'sprint',
            'options': sprints_filter
        }

    if args['ceremony_type']:
        ceremony_type = [{'key': _type.value, 'label': _type.value} for _type in CeremonyType]
        filters['ceremony_type'] = {
            'label': 'Ceremony type',
            'value': 'ceremony_type',
            'options': ceremony_type
        }

    if args['ceremony_status']:
        ceremony_status = [{'key': _type.value.lower().replace(' ', '_'), 'label': _type.value.lower().replace(' ', '_')} for _type in CeremonyStatus]
        filters['ceremony_status'] = {
            'label': 'Status',
            'value': 'status',
            'options': ceremony_status
        }

    return send_response(filters, [], 200, **g.req_data)

@ceremonies.route('/join/<ceremony_id>', methods=['GET'])
def join_ceremony(ceremony_id):
    Ceremony.change_ceremony_status(ceremony_id, CeremonyStatus.CONCLUDED.value)
    return send_response([], [], 200, **g.req_data)

@ceremonies.route('/status/<ceremony_id>', methods=['GET'])
def ceremony_did_not_take_place(ceremony_id):
    '''
    This sets the status as DIDNT_TAKE_PLACE as soon as the countdown finishes. If a user joins the ceremony,
    it will be changed to CONCLUDED and once it's concluded it can't be changed back to DIDNT_TAKE_PLACE
    '''
    ceremony = Ceremony.get_ceremony_by_id(ceremony_id)
    if ceremony['ceremony_status'] == CeremonyStatus.NOT_HAPPENED_YET.value:
        Ceremony.change_ceremony_status(ceremony_id, CeremonyStatus.DIDNT_TAKE_PLACE.value)
    return send_response([], [], 200, **g.req_data)

@ceremonies.route('/<ceremony_id>', methods=['GET'])
def get_ceremony(ceremony_id):
    try:
        ceremony = Ceremony.get_ceremony_by_id(ceremony_id)
        if not ceremony:
            return jsonify({'error': 'Ceremony not found'}), 404
        return jsonify(ceremony), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ceremonies.route('/is_active_ceremony', methods=['GET'])
@use_args(
    {"team_id": fields.Str(required=True), "ceremony_id": fields.Str(required=True)},
    location="query",
)
def get_is_active_ceremony_in_team(args):
    response = Ceremony.is_ceremony_active(args["ceremony_id"])
    return send_response(response, [], 200, **g.req_data)
