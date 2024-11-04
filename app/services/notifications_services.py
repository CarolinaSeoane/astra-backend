from app.models.notification import Notification
from app.models.team import Team


def notify_story_update(old_story, updated_fields, team_id):
    """
    Enviar notificaciones sobre los cambios realizados a la historia, excluyendo
    cambios en `team`, `_id`, y `subscribers`.

    Si se modifica el campo assigned to:
        - el assigned to original va a recibir una sola notificacion indicandole que ya no
        es mas el assigned to de la story.
        - el nuevo assigned to va a recibir una sola notificacion indicandole que tiene una
        nueva story asignada.
    
    Si no se modifica el campo assigned to, el assigned to original recibira tantas notificaciones
    como campor se hayan modificado.
    
    El creator, PO y subscribers de la story recibe tantas notificaciones como campos
    se hayan modificado.
    """
    subscribers = old_story.get("subscribers", [])
    story_id = old_story.get("story_id")
    story_title = old_story.get('title', 'No Title')
    creator_id = old_story.get('creator', {}).get('_id', None)
    po_id = Team.get_product_owner(team_id)
    print("PO:", po_id)
    original_assigned_to = old_story.get('assigned_to', {}).get('_id', None)
    new_assigned_to = original_assigned_to

    original_assign_message = ""
    new_assign_message = ""

    notifications = []

    if "title" in updated_fields:
        old_title = old_story.get("title", "Título antiguo no disponible")
        title_message = f"El título de la historia '{old_title}' se ha cambiado a '{updated_fields['title']}'."
        notifications.append(title_message)

    if "description" in updated_fields:
        description_message = "La descripción de la historia ha sido actualizada. Clickea para ver mas."
        notifications.append(description_message)

    if "acceptance_criteria" in updated_fields:
        criteria_message = "Se han actualizado los criterios de aceptación de la historia."
        notifications.append(criteria_message)

    if "assigned_to" in updated_fields:
        new_assigned_to = updated_fields["assigned_to"]["_id"]
        original_assign_message = f"Te han desasignado la tarea '{story_title}'."
        new_assign_message = f"Se te ha asignado la historia '{story_title}'."
        assign_message = "Se ha cambiado el usuario asignado a la historia."
        notifications.append(assign_message)

    if "epic" in updated_fields:
        epic_message = f"Se ha actualizado la épica de la historia a '{updated_fields['epic']['title']}'."
        notifications.append(epic_message)

    if "sprint" in updated_fields:
        sprint_message = f"Se ha cambiado el sprint de la historia a {updated_fields['sprint']['name']}."
        notifications.append(sprint_message)

    if "estimation" in updated_fields:
        estimation_message = f"Se ha cambiado la estimación de la historia a {updated_fields['estimation']} puntos."
        notifications.append(estimation_message)

    if "priority" in updated_fields:
        priority_message = f"Se ha cambiado la prioridad de la historia a {updated_fields['priority']}."
        notifications.append(priority_message)

    if "tasks" in updated_fields:
        tasks_message = "Se han actualizado las tareas de la historia."
        notifications.append(tasks_message)

    if "story_type" in updated_fields:
        story_type_message = f"El tipo de historia ha sido actualizado a '{updated_fields['story_type']}'"
        notifications.append(story_type_message)

    print(f"created the following notifications {notifications}")

    if original_assigned_to == new_assigned_to:
        # se le envian todas las notificaciones al assigned to
        print("the assigned to didnt change. sending all notifications to them")
        send_multiple_notifications(
            notifications=notifications,
            story=old_story,
            team_id=team_id,
            to_notify=original_assigned_to,
            title=f"{story_id} - {story_title}",
            assigned_to=original_assigned_to
        )
    else:
        # se le envia una notificacion a cada uno
        print("theres a new assigned to. sending two notifications, one for each")
        Notification.create_notification(
            owner_id=new_assigned_to,
            title=f"{story_id} - {story_title}",
            msg=original_assign_message,
            story=old_story,
            assigned_to=original_assigned_to,
            team_id=team_id
        )
        Notification.create_notification(
            owner_id=new_assigned_to,
            title=f"{story_id} - {story_title}",
            msg=new_assign_message,
            story=old_story,
            assigned_to=new_assigned_to,
            team_id=team_id
        )

    # send all notifications to creator
    if creator_id not in (original_assigned_to, new_assigned_to):
        print("notifying creator")
        send_multiple_notifications(
            notifications=notifications,
            story=old_story,
            team_id=team_id,
            to_notify=creator_id,
            title=f"{story_id} - {story_title}",
        )

    # send all notifications to po
    if po_id and po_id not in (creator_id, original_assigned_to, new_assigned_to):
        print("notifying po")
        send_multiple_notifications(
            notifications=notifications,
            story=old_story,
            team_id=team_id,
            to_notify=po_id,
            title=f"{story_id} - {story_title}",
        )

    # send all notifications to all subscribers
    for subscriber in subscribers:
        print("notifying subscribers")
        if subscriber in (po_id, creator_id, original_assigned_to, new_assigned_to):
            continue
        send_multiple_notifications(
            notifications=notifications,
            story=old_story,
            team_id=team_id,
            to_notify=subscriber,
            title=f"{story_id} - {story_title}",
        )

def send_multiple_notifications(notifications, story, team_id, to_notify, title, assigned_to=None):
    for notification in notifications:
        Notification.create_notification(
            owner_id=to_notify,
            msg=notification,
            story=story,
            assigned_to=assigned_to,
            team_id=team_id,
            title=title
        )
