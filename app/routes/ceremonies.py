from flask import Blueprint, request, g
from webargs.flaskparser import use_args
from webargs import fields
from datetime import datetime

from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.ceremony import Ceremony
from app.models.configurations import CeremonyType, CeremonyStatus
from app.models.sprint import Sprint
from app.services.astra_scheduler import get_quarter


ceremonies = Blueprint("ceremonies", __name__)

excluded_routes = [
    
]

@ceremonies.before_request
def apply_validate_user_is_active_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_active_member_of_team()

@ceremonies.route('/sprint/<sprint_id>', methods=['GET'])
def team_ceremonies(sprint_id):
    ceremonies = [
        {
            'name': 'Standup begins',
            'date': '2024-08-01T20:28:30',
            'in_progress': False
        },
        {
            'name': 'Standup',
            'date': '2024-08-01T20:28:35',
            'in_progress': True
        },
        {
            'name': 'Retro begins',
            'date': '2024-08-01T20:28:50',
            'in_progress': False
        },
        {
            'name': 'Retro',
            'date': '2024-08-01T20:28:55',
            'in_progress': True
        },
    ]

    Ceremony.get_sprint_ceremonies(sprint_id)

    return send_response(ceremonies, [], 200, **g.req_data)

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