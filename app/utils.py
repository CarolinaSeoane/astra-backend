from flask import jsonify


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
    pass

def gantt_format(stories_dict):
    pass