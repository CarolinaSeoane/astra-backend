from flask import Blueprint, request, g
from webargs.flaskparser import use_args
from webargs import fields
from datetime import datetime

from app.utils import send_response, apply_banner_format
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.ceremony import Ceremony
from app.models.configurations import CeremonyType, CeremonyStatus
from app.models.sprint import Sprint
from app.services.astra_scheduler import get_quarter
from app.models.user import User
from app.services.google_meet import list_conference_records

ceremonies = Blueprint("ceremonies", __name__)

excluded_routes = [
    
]

@ceremonies.before_request
def apply_validate_user_is_active_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_active_member_of_team()

@ceremonies.route('/banner', methods=['GET'])
def team_ceremonies():
    ceremonies = Ceremony.get_upcoming_ceremonies_by_team_id(g.team_id)
    banner_formatted_ceremonies = apply_banner_format(ceremonies)
    return send_response(banner_formatted_ceremonies, [], 200, **g.req_data)

@ceremonies.route('', methods=['GET'])
@use_args({
    'sprint': fields.Str(required=False),
    'ceremony_type': fields.Str(required=False),
    'ceremony_status': fields.Str(required=False),
    }, location='query')
def ceremonies_list(args):
    ceremonies = Ceremony.get_ceremonies_by_team_id(g.team_id, **args)
    return send_response(ceremonies, [], 200, **g.req_data)

@ceremonies.route('/meet/data/<ceremony_id>', methods=['GET'])
def get_ceremonies_meet_data(ceremony_id):
    print('getting meet data for ceremony_id: ', ceremony_id)
    user_doc = User.get_user_by({'email': g.email}, True)
    user_obj = User(**user_doc)
    ceremony = Ceremony.get_ceremonies_by_team_id(g.team_id, ceremony_id=ceremony_id)[0]
    print(ceremony)
    list_conference_records(user_obj.access_token, user_obj.refresh_token, ceremony)
    return send_response([], [], 200, **g.req_data)

@ceremonies.route("/filters", methods=['GET'])
@use_args({
    ## available filters
    'sprints': fields.Boolean(required=False, missing=True),
    'ceremony_type': fields.Boolean(required=False, missing=True),
    'ceremony_status': fields.Boolean(required=False, missing=True),
    ## customization
    'quarter': fields.Integer(required=False, missing=get_quarter(datetime.today())),
    'year': fields.Integer(required=False, missing=datetime.today().year),
    'future': fields.Str(required=False, missing=False),
    }, location='query')
def filters(args):
    sprints_filter = []
    ceremony_type = []
    ceremony_status = []
    filters = {}

    if args['sprints']:
        sprints = Sprint.get_sprints(g.team_id, args['quarter'], args['year'], args['future'])

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
        ceremony_status = [{'key': _type.value, 'label': _type.value} for _type in CeremonyStatus]
        filters['ceremony_status'] = {
            'label': 'Status',
            'value': 'status',
            'options': ceremony_status
        }

    return send_response(filters, [], 200, **g.req_data)

@ceremonies.route('/join/<ceremony_id>', methods=['GET'])
def join_ceremony(ceremony_id):
    print('joining ceremony ', ceremony_id)
    # ceremonies = Ceremony.get_ceremonies_by_team_id(g.team_id, **args)
    return send_response([], [], 200, **g.req_data)