from bson import ObjectId
from flask import jsonify

from app.models.task import Status


def send_response(data, errors, status_code, method, endpoint):
    payload = {
        'meta': {
            'method': method,
            'endpoint': endpoint
        },
        'data': data,
        'errors': errors
    }
    return jsonify(payload), status_code

def kanban_format(stories_dict):
    kanban_columns = [
        {"key": "stories", "quantity": 0},
        {"key": "NotStarted", "quantity": 0},
        {"key": "Doing", "quantity": 0},
        {"key": "Done", "quantity": 0},
        {"key": "Blocked", "quantity": 0}
    ]
    kanban_dict = {col['key']: col for col in kanban_columns}
    for story in stories_dict:
        story['tasksNotStarted'] = []
        story['tasksDoing'] = []
        story['tasksDone'] = []
        story['tasksBlocked'] = []

        for task in story['tasks']:
            status = task['status'].replace(" ", "")
            story[f'tasks{status}'].append(task['title'])
            if status in kanban_dict:
                kanban_dict[status]['quantity'] += 1

        story.pop('tasks')

    kanban_data = {
        "stories": stories_dict,
        "kanban_columns": kanban_columns
    }
    return kanban_data

def list_format(stories_dict):
    for story in stories_dict:
        total_tasks = 0
        tasks_completed = 0

        for task in story.get('tasks', []):
            total_tasks += 1
            if task['status'] == Status.DONE.value:
                tasks_completed += 1

        try:
            completness = round(tasks_completed/total_tasks * 100)
            story.pop('tasks')
        except Exception:
            completness = 0

        story['completeness'] = completness
    return stories_dict

def gantt_format(stories_dict):
    pass

def apply_banner_format(ceremonies):
    formatted_ceremonies = []
    for ceremony in ceremonies:
        formatted_ceremonies.extend([
            {
                'name': f"{ceremony['ceremony_type']} begins",
                'date': ceremony['starts']['$date'][:-1],
                'in_progress': False
            },
            {
                '_id': ceremony['_id'],
                'name': f"{ceremony['ceremony_type']}",
                'date': ceremony['ends']['$date'],
                'in_progress': True,
                'google_meet_link': ceremony['google_meet_config']["meetingUri"]
            }
        ])
    return formatted_ceremonies

def get_current_quarter(date):
    month = date.month
    if month in [1, 2, 3]:
        return 1
    if month in [4, 5, 6]:
        return 2
    if month in [7, 8, 9]:
        return 3
    return 4

def mongo_query(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"mongo error {e}")
            return {"message": [], "error": f"Unable to complete operation: {e}", "status": 500}
    return wrapper

def try_to_convert_to_object_id(to_convert):
    if isinstance(to_convert, ObjectId):
        return to_convert
    if to_convert is None:
        return ''
    try:
        to_convert = ObjectId(to_convert["$oid"])
    except Exception as e:
        print(f"error converting to object id: {e}")
    return to_convert
