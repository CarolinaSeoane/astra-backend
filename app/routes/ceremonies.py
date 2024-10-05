from flask import Blueprint, request

from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team


ceremonies = Blueprint("ceremonies", __name__)

excluded_routes = [
    
]

@ceremonies.before_request
def apply_validate_user_is_active_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_active_member_of_team()

@ceremonies.route('/ceremonies', methods=['GET'])
def team_ceremonies():
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

    return send_response(ceremonies, [], 200, **g.req_data)
