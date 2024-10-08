import requests
from datetime import datetime
from bson import ObjectId
from app.models.notification import Notification
from app.models.team import Team 


def notify_story_update(story, updated_fields, team_id):
    """
    Enviar notificaciones sobre los cambios realizados a la historia, excluyendo cambios en `team`, `_id`, y `subscribers`.
    Si se modifica el campo `comments`, enviará el contenido del comentario.
    """
    print(f"Notificando actualización de historia. Old Story: {story}, Updated Fields: {updated_fields}, Team ID: {team_id}")
    
    # Obtener el user_id del creador de la historia
    creator_id_str = Notification._extract_id_string(story.get('creator', {}).get('_id', ''))
    
    # Obtener suscriptores y asignados
    subscribers = story.get('subscribers', [])  
    assigned_to = story.get('assigned_to', {})  
    assigned_to_id_str = Notification._extract_id_string(assigned_to.get('_id', ''))  

    notifications = []
        
    #if 'assigned_to' in updated_fields:
    #    new_assigned_user = updated_fields['assigned_to']
    #    new_assigned_user_str = Notification._extract_id_string(updated_fields['assigned_to'].get('_id', ''))
    #    new_assigned_user_name = new_assigned_user.get('name', 'Usuario')  # Obtener nombre del nuevo usuario asignado
    #    assign_message = f"Se ha cambiado el usuario asignado a la historia {story.get('title', 'No Title')}."
    #    notifications.append((new_assigned_user_str, assign_message))
        
    if 'title' in updated_fields:
        title_message = f"El título de la historia se ha cambiado a '{updated_fields['title']}'."
        notifications.append((assigned_to_id_str, title_message))

    if 'acceptance_criteria' in updated_fields:
        criteria_message = f"Se han actualizado los criterios de aceptación de la historia '{story.get('title', 'No Title')}'."
        notifications.append((assigned_to_id_str, criteria_message))

    if 'assigned_to' in updated_fields:
        new_assigned_user = updated_fields['assigned_to']
        new_assigned_user_str = Notification._extract_id_string(new_assigned_user.get('_id', ''))
        assign_message = f"Se ha cambiado el usuario asignado a la historia '{story.get('title', 'No Title')}'."
        notifications.append((new_assigned_user_str, assign_message))

    if 'epic' in updated_fields:
        epic_message = f"Se ha actualizado la épica de la historia '{story.get('title', 'No Title')}'."
        notifications.append((assigned_to_id_str, epic_message))

    if 'sprint' in updated_fields:
        sprint_message = f"Se ha cambiado el sprint de la historia '{story.get('title', 'No Title')}'."
        notifications.append((assigned_to_id_str, sprint_message))

    if 'estimation' in updated_fields:
        estimation_message = f"Se ha cambiado la estimación de la historia '{story.get('title', 'No Title')}' a {updated_fields['estimation']} puntos."
        notifications.append((assigned_to_id_str, estimation_message))

    if 'tags' in updated_fields:
        tags_message = f"Se han actualizado las etiquetas de la historia '{story.get('title', 'No Title')}'."
        notifications.append((assigned_to_id_str, tags_message))

    if 'priority' in updated_fields:
        priority_message = f"Se ha cambiado la prioridad de la historia '{story.get('title', 'No Title')}' a {updated_fields['priority']}."
        notifications.append((assigned_to_id_str, priority_message))

    if 'tasks' in updated_fields:
        tasks_message = f"Se han actualizado las tareas de la historia '{story.get('title', 'No Title')}'."
        notifications.append((assigned_to_id_str, tasks_message))

    if 'estimation_method' in updated_fields:
        method_message = f"Se ha cambiado el método de estimación a '{updated_fields['estimation_method']}' para la historia '{story.get('title', 'No Title')}'."
        notifications.append((assigned_to_id_str, method_message))
    #for field in updated_fields.items():
    #    if field, new_value not in ['team', '_id', 'subscribers', 'comments']:
    #for field, new_value in updated_fields.items():
    #    if field not in ['team', '_id', 'subscribers', 'comments']:
    #        message = f"El campo {field} de la historia {story.get('title', 'No Title')} ha sido actualizado a {new_value}."
    #        notifications.append((assigned_to_id_str, message))
    #for field, new_value in updated_fields.items():
    #    if field not in ['team', '_id', 'subscribers', 'comments']:
    #        # Verifica si el nuevo valor es un objeto o una lista
    #        message = f"El campo {field} de la historia {story.get('title', 'No Title')} ha sido actualizado."
    #        notifications.append((assigned_to_id_str, message))
        
    # Enviar notificaciones al asignado
    for user_id_str, message in notifications:
        if user_id_str and len(user_id_str) == 24:
            try:
                Notification.create_notification({
                    'user_id': ObjectId(user_id_str),
                    'message': message,
                    'story_id': story.get('_id', 'No ID'),
                    'creator': ObjectId(creator_id_str),
                    'assigned_to': ObjectId(user_id_str) if user_id_str == assigned_to_id_str else None,
                    'team_id': team_id,
                    'created_at': datetime.now().isoformat(),
                    'viewed_by': []
                })
                print(f"Notificación enviada al asignado {user_id_str}: {message}")
            except Exception as e:
                print("Error al crear notificación:", e)

    # Enviar notificaciones al creador
    if creator_id_str and len(creator_id_str) == 24:
        for user_id_str, message in notifications:
            if user_id_str != creator_id_str:  # Evitar enviar al creador
                try:
                    Notification.create_notification({
                        'user_id': ObjectId(creator_id_str),
                        'message': message,
                        'story_id': story.get('_id', 'No ID'),
                        'creator': ObjectId(creator_id_str),
                        'assigned_to': ObjectId(user_id_str) if 'assigned_to' in updated_fields and new_assigned_user_str != creator_id_str else None,
                        'team_id': team_id,
                        'created_at': datetime.now().isoformat(),
                        'viewed_by': []
                    })
                    print(f"Notificación enviada al creador {creator_id_str}: {message}")
                except Exception as e:
                    print("Error al crear notificación:", e)

    # Enviar notificaciones a suscriptores
    for subscriber in subscribers:
            subscriber_id = subscriber.get('$oid')  # Obtener el valor del ID
            if subscriber_id and len(subscriber_id) == 24:  # Verificar que el ID sea válido
                for user_id_str, message in notifications:
                #message = f"La historia '{story['title']}' ha sido actualizada con los siguientes cambios: {updated_fields}"
                    try:
                        Notification.create_notification({
                            'user_id': ObjectId(subscriber_id),  # Convertir a ObjectId
                            'message': message,
                            'story_id': story.get('_id', 'No ID'),
                            'creator': ObjectId(creator_id_str),
                            'assigned_to': ObjectId(user_id_str) if 'assigned_to' in updated_fields else None,
                            'team_id': team_id,
                            'created_at': datetime.now().isoformat(),
                            'viewed_by': []
                        })
                        print(f"Notificación enviada a subscriptor {subscriber_id}: {message}")
                    except Exception as e:
                        print("Error al crear notificación:", e)

    # Enviar notificación al Product Owner si corresponde
    po_id = get_product_owner_id(team_id)
    print("PO:",po_id)# Asegúrate de tener una función que obtenga el ID del PO
    if po_id:
        for message in notifications:
            try:
                Notification.create_notification({
                    'user_id': ObjectId(po_id),  # Enviar notificación al PO, no al creador
                    'message': message,  
                    'story_id': story.get('_id', 'No ID'),
                    'creator': ObjectId(creator_id_str),  # ID del creador de la historia
                    'assigned_to': ObjectId(user_id_str) if 'assigned_to' in updated_fields else None,
                    'team_id': team_id,
                    'created_at': datetime.now().isoformat(),
                    'viewed_by': []
                })
                print(f"Notificación enviada al Product Owner {po_id}: {message}")
            except Exception as e:
                print("Error al crear notificación:", e)

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

def get_product_owner_id(team_id):
    
    team = Team.get_team(ObjectId(team_id))
    
    if team:
        
        for member in team.get('members', []):
            if member.get('role') == 'Product Owner':
                
                po_id = member.get('_id')
                
                if isinstance(po_id, dict) and '$oid' in po_id:
                    return ObjectId(po_id['$oid']) 
                return po_id 
    
    return None