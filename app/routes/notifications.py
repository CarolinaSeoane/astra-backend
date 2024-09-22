from bson import ObjectId
from flask import Blueprint, request, jsonify, g
from app.models.notification import Notification
from app.utils import send_response
notifications = Blueprint('notifications', __name__)

@notifications.route('/create', methods=['POST'])
def create_notification():
    try:
        data = request.json

        # Convertir los IDs de cadena a ObjectId
        user_id = ObjectId(data.get('user_id'))
        story_id = ObjectId(data.get('story_id'))
        creator = ObjectId(data.get('creator'))
        assigned_to = ObjectId(data.get('assigned_to')) if data.get('assigned_to') else None
        created_at = data.get('created_at')
        viewed = data.get('viewed', False)

        # Crear el documento de notificación
        notification_data = {
            'user_id': user_id,
            'message': data.get('message'),
            'story_id': story_id,
            'creator': creator,
            'assigned_to': assigned_to,
            'created_at': created_at,
            'viewed': viewed  # Campo por defecto
        }
        
        # Validación básica
        if not all([notification_data.get('user_id'), notification_data.get('message'), notification_data.get('story_id'), notification_data.get('creator')]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Crear notificación en la base de datos
        result = Notification.create_notification(notification_data)
        
        # Convertir el resultado a un formato serializable
        notification = {
            'id': str(result.inserted_id),
            'user_id': str(user_id),
            'message': data.get('message'),
            'story_id': str(story_id),
            'creator': str(creator),
            'assigned_to': str(assigned_to) if assigned_to else None,
            'created_at': created_at,
            'viewed': viewed  # Campo por defecto
        }

        return jsonify({'message': 'Notification created successfully', 'notification': notification}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#@notifications.route('/mark_as_viewed', methods=['PATCH'])
#def mark_as_viewed():
#    try:
#        data = request.json
#        user_id = data.get('user_id')
#        notification_ids = data.get('notification_ids')

        # Validación básica
#        if not user_id or not notification_ids:
#            return jsonify({'error': 'user_id and notification_ids are required'}), 400

        # Convertir los IDs de cadena a ObjectId
#        try:
#            notification_ids = [ObjectId(id) for id in notification_ids]
#            user_id = ObjectId(user_id)
#        except Exception as e:
#            return jsonify({'error': 'Invalid ID format'}), 400

        # Marcar las notificaciones como vistas
#        result = Notification.mark_as_viewed(user_id, notification_ids)

#        if result.modified_count > 0:
#            return jsonify({'message': 'Notifications marked as viewed'}), 200
#        else:
#            return jsonify({'error': 'No notifications updated'}), 404

#    except Exception as e:
#        return jsonify({'error': str(e)}), 500

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
    
    notifications = Notification.get_notifications_for_user(user_id)
    return send_response(notifications, [], 200, **g.req_data)

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

    notifications = Notification.get_creator_notifications(user_id)
    return send_response(notifications, [], 200, **g.req_data)

@notifications.route('/assigned', methods=['GET'])
def get_assigned_user_notifications():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')

    if not user_id or not team_id:
        return send_response([], ['Missing user_id or team_id'], 400, **g.req_data)

    notifications = Notification.get_assigned_user_notifications(user_id)
    return send_response(notifications, [], 200, **g.req_data)    

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