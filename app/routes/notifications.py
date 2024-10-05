from bson import ObjectId
from flask import Blueprint, request, jsonify, g
from app.models.notification import Notification
from app.utils import send_response

notifications = Blueprint('notifications', __name__)

@notifications.route('/create', methods=['POST'])
def create_notification():
    notification_data = request.json


    if not all(key in notification_data for key in ['user_id', 'message', 'story_id', 'creator', 'team_id']):
        return jsonify({'error': 'Faltan datos necesarios'}), 400

    try:
        notification = Notification(**notification_data)
        Notification.create_notification(notification.__dict__)
        return jsonify({'message': 'Notificación creada con éxito'}), 201
    except Exception as e:
        return jsonify({'error': f'Error al crear la notificación: {e}'}), 500

@notifications.route('/mark_as_viewed', methods=['POST'])
def mark_notifications_as_viewed():
    user_id = request.json.get('user_id')
    team_id = request.json.get('team_id')
    filter_type = request.json.get('filter_type')

    if not user_id or not team_id or not filter_type:
        return jsonify({'error': 'Missing parameters'}), 400

    Notification.mark_notifications_as_viewed(user_id, team_id, filter_type)
    return jsonify({'message': 'Notifications marked as viewed'})   

@notifications.route('/', methods=['GET'])
def get_user_notifications():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')
    
    if not user_id or not team_id:
        return send_response([], ['Missing user_id or team_id'], 400, **g.req_data)
    
    try:
        notifications = Notification.get_notifications_for_user(user_id, team_id)  
        return send_response(notifications, [], 200, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to get user notifications: {e}"], 500, **g.req_data)

@notifications.route('unread', methods=['GET'])
def get_unread_notifications():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')

    if not user_id or not team_id:
        return send_response([], ['Missing user_id or team_id'], 400, **g.req_data)

    try:
        unread_count = Notification.count_unread_notifications(user_id, team_id)
        return send_response({"unreadCount": unread_count}, [], 200, **g.req_data)
    except Exception as e:
        print(f"Error: {e}")
        return send_response([], ['Internal Server Error'], 500, **g.req_data)

@notifications.route('creator', methods=['GET'])
def get_creator_notifications():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')

    if not user_id or not team_id:
        return send_response([], ['Missing user_id or team_id'], 400, **g.req_data)

    try:
        notifications = Notification.get_creator_notifications(user_id, team_id)  
        return send_response(notifications, [], 200, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to get creator notifications: {e}"], 500, **g.req_data)

@notifications.route('/assigned', methods=['GET'])
def get_assigned_user_notifications():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')  

    if not user_id or not team_id:
        return send_response([], ["User ID and Team ID are required."], 400, **g.req_data)

    try:
        notifications = Notification.get_assigned_user_notifications(user_id, team_id)
        return send_response(notifications, [], 200, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to get notifications: {e}"], 500, **g.req_data)  

@notifications.route('/assigned/count', methods=['GET'])
def get_assigned_notifications_count():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')
    count = Notification.count_assigned_notifications(user_id, team_id)
    return jsonify({'count': count})

@notifications.route('/creator/count', methods=['GET'])
def get_created_notifications_count():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')
    count = Notification.count_created_notifications(user_id, team_id)
    return jsonify({'count': count})

@notifications.route('/count', methods=['GET'])
def get_all_notifications_count():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')
    count = Notification.count_all_notifications(user_id, team_id)
    return jsonify({'count': count})

@notifications.route('/unread/count', methods=['GET'])
def get_unread_notifications_count():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')
    count = Notification.count_unread_notifications(user_id, team_id)
    return jsonify({'count': count})

@notifications.route('/subscribed', methods=['GET'])
def get_subscribed_notifications():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')
    print("User ID:", user_id)  
    print("Team ID:", team_id)  
    if not user_id or not team_id:
        return send_response([], ['Missing user_id or team_id'], 400, **g.req_data)

    try:
        notifications = Notification.get_subscribed_notifications(user_id, team_id)
        return send_response(notifications, [], 200, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to get subscribed notifications: {e}"], 500, **g.req_data)
    
@notifications.route('/team/edits', methods=['GET'])
def get_story_edits():
    team_id = request.args.get('team_id')
    user_id = request.args.get('user_id')
    if not team_id:

        method = request.method
        endpoint = request.path
        return send_response([], ['Missing team_id'], 400, method=method, endpoint=endpoint)
    
    if not user_id: 
        method = request.method
        endpoint = request.path
        return send_response([], ['Missing user_id'], 400, method=method, endpoint=endpoint)
    
    try:
        edits = Notification.get_team_story_edits(team_id, user_id)
        return send_response(edits, [], 200, method=request.method, endpoint=request.path)
    except Exception as e:
        return send_response([], [f"Failed to get team story edits: {e}"], 500, method=request.method, endpoint=request.path)
    
@notifications.route('/subscribed/count', methods=['GET'])
def get_subscribed_notifications_count():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')

    if not user_id or not team_id:
        return send_response([], ['Missing user_id or team_id'], 400, **g.req_data)

    try:

        unread_count = Notification.count_subscribed_notifications(user_id, team_id)
        return send_response({'unreadCount': unread_count}, [], 200, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to count unread subscribed notifications: {e}"], 500, **g.req_data)
    
@notifications.route('/team/edits/count', methods=['GET'])
def get_story_edits_count():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')

    if not user_id or not team_id:
        return send_response([], ['Missing user_id or team_id'], 400)

    count = Notification.count_team_story_edits(user_id, team_id)
    return jsonify({'count': count})