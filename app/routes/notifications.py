from flask import Blueprint, request, jsonify, g
from webargs import fields

from app.models.notification import (
    Notification,
    get_assigned_user_notifications,
    get_creator_notifications,
    get_subscribed_notifications,
    get_team_story_edits,
)
from app.routes.utils import validate_user_is_active_member_of_team
from app.utils import send_response


notifications = Blueprint('notifications', __name__)

get_notifications_args = {
    'team_id': fields.Str(required=True),
    'user_id': fields.Str(required=True)
}

excluded_routes = []

@notifications.before_request
def apply_validate_user_is_active_member_of_team():
    for excluded_route in excluded_routes:
        if (
            request.path.startswith(excluded_route['route'])
            and (request.method in excluded_route['methods'])
        ):
            return None

    return validate_user_is_active_member_of_team()

@notifications.route('/mark_as_viewed/<filter_type>', methods=['POST'])
def mark_notifications_as_viewed(filter_type):
    Notification.mark_notifications_as_viewed(g._id, g.team_id, filter_type)
    return jsonify({'message': 'Notifications marked as viewed'})

filter_method = {
    "assigned": get_assigned_user_notifications,
    "creator": get_creator_notifications,
    "subscribed": get_subscribed_notifications,
    "all": get_team_story_edits
}

@notifications.route("/<filter_type>", methods=["GET"])
def get_notifications(filter_type):
    method = filter_method[filter_type]
    try:
        notifications = method(g._id, g.team_id)
        return send_response(notifications, [], 200, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to get creator notifications: {e}"], 500, **g.req_data)

@notifications.route("/counts", methods=["GET"])
def get_notifications_count():
    assigned_count = 0
    created_count = 0
    subscribed_count = 0
    team_edits_count = 0
    try:
        assigned_count = Notification.count_assigned_notifications(g._id, g.team_id)
        created_count = Notification.count_created_notifications(g._id, g.team_id)
        subscribed_count = Notification.count_subscribed_notifications(g._id, g.team_id)
        team_edits_count = Notification.count_team_story_edits(g._id, g.team_id)
    except Exception as e:
        return send_response([], [f"Failed to count notifications: {e}"], 500, **g.req_data)
    counts = {
        "assigned_count": assigned_count,
        "created_count": created_count,
        "subscribed_count": subscribed_count,
        "team_edits_count": team_edits_count,
    }
    return send_response(counts, [], 200, **g.req_data)
