import requests
from datetime import datetime
from bson import ObjectId
from app.models.notification import Notification
from app.models.team import Team 


def notify_story_update(story, updated_fields, team_id, user_id):
    """
    Enviar notificaciones sobre los cambios realizados a la historia, excluyendo cambios en `team`, `_id`, y `subscribers`.
    Si se modifica el campo `comments`, enviará el contenido del comentario.

    """
    creator_id_str = Notification._extract_id_string(story.get('creator', {}).get('_id', ''))
    subscribers = story.get('subscribers', [])  
    assigned_to = story.get('assigned_to', {})  
    assigned_to_id_str = Notification._extract_id_string(assigned_to.get('_id', ''))  

    notifications = []
    
    excluded_fields = ['team', '_id', 'subscribers']

    
    if 'comments' in updated_fields:
        comments_message = f"Un nuevo comentario fue agregado a la historia {story.get('title', 'No Title')}: {updated_fields['comments']}."
        notifications.append(comments_message)
        
    if 'assigned_to' in updated_fields:
        new_assigned_user_str = Notification._extract_id_string(updated_fields['assigned_to'].get('_id', ''))
        assign_message = f"Has sido asignado a la historia {story.get('title', 'No Title')}."
        notifications.append(assign_message)
    
    
    for field in updated_fields.items():
        if field not in excluded_fields and field != 'comments':
            message = f"El campo {field} de la historia {story.get('title', 'No Title')} ha sido actualizado."
            notifications.append(message)

    
    if new_assigned_user_str and len(new_assigned_user_str) == 24:
        Notification.create_notification({
            'user_id': ObjectId(new_assigned_user_str),
            'message': assign_message,
            'story_id': story.get('_id', 'No ID'),
            'creator': ObjectId(creator_id_str),
            'assigned_to': ObjectId(new_assigned_user_str),
            'team_id': team_id,
            'created_at': datetime.now().isoformat(),
            'viewed_by': []
        })
   
    
    if assigned_to_id_str and len(assigned_to_id_str) == 24:
        for message in notifications:
            Notification.create_notification({
                'user_id': ObjectId(assigned_to_id_str),
                'message': message,
                'story_id': story.get('_id', 'No ID'),
                'creator': ObjectId(creator_id_str),
                'assigned_to': ObjectId(assigned_to_id_str),
                'team_id': team_id,
                'created_at': datetime.now().isoformat(),
                'viewed_by': []
            })
    
    
    if creator_id_str and len(creator_id_str) == 24:
        for message in notifications:
            Notification.create_notification({
                'user_id': ObjectId(creator_id_str),
                'message': message,
                'story_id': story.get('_id', 'No ID'),
                'creator': ObjectId(creator_id_str),
                'assigned_to': ObjectId(new_assigned_user_str) if 'assigned_to' in updated_fields and new_assigned_user_str != creator_id_str else None,
                'team_id': team_id,
                'created_at': datetime.now().isoformat(),
                'viewed_by': []
            })

    
    for subscriber in subscribers:
        subscriber_id_str = Notification._extract_id_string(subscriber.get('_id', ''))
        creator_id_str=Notification._extract_id_string(story.get('creator', {}).get('_id', ''))
        if subscriber_id_str and len(subscriber_id_str) == 24:
            for message in notifications:
                Notification.create_notification({
                    'user_id': ObjectId(subscriber_id_str),
                    'message': message,
                    'story_id': story.get('_id', 'No ID'),
                    'creator': creator_id_str,
                    'assigned_to': ObjectId(new_assigned_user_str) if 'assigned_to' in updated_fields else None,
                    'team_id': team_id,
                    'created_at': datetime.now().isoformat(),
                    'viewed_by': []
                })

    if is_product_owner(user_id, team_id):
        for message in notifications:
            Notification.create_notification({
                'user_id': ObjectId(user_id),
                'message': f"(PO) {message}",  
                'story_id': story.get('_id', 'No ID'),
                'creator': ObjectId(creator_id_str),
                'assigned_to': ObjectId(new_assigned_user_str) if 'assigned_to' in updated_fields else None,
                'team_id': team_id,
                'created_at': datetime.now().isoformat(),
                'viewed_by': []
            })


def is_product_owner(user_id, team_id):

    endpoint_url = f"http://127.0.0.1:5000/teams/product_owner/role_check/{user_id}"
    try:
        params = {'team_id': team_id}
        response = requests.get(endpoint_url, params=params) 
        if response.status_code == 200:
            result = response.json()
            return result.get('data') 
        else:
            print(f"Error al solicitar el estado de Product Owner: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el endpoint de Product Owner: {e}")
        return False