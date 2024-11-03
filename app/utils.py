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
    for story in stories_dict:
        story['tasksNotStarted'] = []
        story['tasksDoing'] = []
        story['tasksDone'] = []
        story['tasksBlocked'] = []

        for task in story['tasks']:
            status = task['status'].replace(" ", "")
            story[f'tasks{status}'].append(task['title'])

        story.pop('tasks')

    return stories_dict

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

def get_current_quarter(date):
    month = date.month
    if month in [1, 2, 3]:
        return 1
    elif month in [4, 5, 6]:
        return 2
    elif month in [7, 8, 9]:
        return 3
    else:
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
