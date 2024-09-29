from flask import request, g
from bson import ObjectId

from app.models.user import User
from app.utils import send_response


def validate_user_is_active_member_of_team():
    '''
    This validation runs before any request made to /teams routes and after token validation
    '''
    if request.method=='OPTIONS':
        return None

    try:
        team_id = request.args['team_id']
    except Exception:
        return send_response([], ["Unprocessable Entity. Missing team_id in query parameters"], 422, **g.req_data)

    try:
        team_id = ObjectId(team_id)
    except Exception:
        return send_response([], [f"Team id {team_id} is not valid"], 403, **g.req_data)

    if not User.is_user_in_team(g._id, team_id):
        return send_response([], ["Forbidden. User is not authorized to access this resource"], 403, **g.req_data)

    g.team_id = team_id
