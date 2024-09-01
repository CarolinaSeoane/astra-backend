from flask import Blueprint, g, request
from webargs.flaskparser import use_args
from webargs import fields
import datetime
import random

from app.models.story import Story, Priority, Type
from app.utils import send_response, get_current_quarter
from app.routes.utils import validate_user_is_member_of_team
from app.models.team import Team
from app.models.sprint import Sprint
from app.models.epic import Epic
from app.models.settings import Settings
from app.models.task import Task


stories = Blueprint("stories", __name__)

excluded_routes = [
    '/stories/fields'
]

@stories.before_request
def apply_validate_user_is_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_member_of_team()

@stories.route("/<view_type>", methods=['GET'])
@use_args({
    'sprint': fields.Str(required=False),
    'assigned_to': fields.Str(required=False),
    'epic': fields.Str(required=False),
    'priority': fields.Str(required=False),
    'story_type': fields.Str(required=False),
    'story_id': fields.Str(required=False)
    }, location='query')
def stories_list(args, view_type):
    stories = Story.get_stories_by_team_id(g.team_id, view_type, **args)
    return send_response(stories, [], 200, **g.req_data)

@stories.route("/fields", methods=['GET'])
@use_args({"sections": fields.Boolean(required=False, missing=False)}, location='query')
def story_fields(args):
    fields = Story.get_story_fields(args["sections"])
    return send_response(fields, [], 200, **g.req_data)

@stories.route("/filters", methods=['GET'])
@use_args({
    ## available filters
    'sprints': fields.Boolean(required=False, missing=True),
    'members': fields.Boolean(required=False, missing=True),
    'epics': fields.Boolean(required=False, missing=True),
    'priority': fields.Boolean(required=False, missing=True),
    'story_type': fields.Boolean(required=False, missing=True),
    'estimation': fields.Boolean(required=False, missing=True),
    ## customization
    'quarter': fields.Str(required=False, missing=str(get_current_quarter(datetime.datetime.today()))), # affects sprints (TODO: should affect epics too!!!!)
    'year': fields.Str(required=False, missing=str(datetime.datetime.today().year)), # affects sprints (TODO: should affect epics too!!!!)
    'future': fields.Str(required=False, missing=False), # affects sprints (TODO: should affect epics too!!!!)
    }, location='query')
def filters(args):
    sprints_filter = []
    members_filter = []
    epics_filter = []
    priority = []
    story_type = []
    estimation = []
    filters = {}
    
    if args['sprints']:
        sprints = Sprint.get_sprints(g.team_id, args['quarter'], args['year'], args['future'])
        for sprint in sprints:
            sprint_option = {
                'key': sprint['_id']['$oid'],
                'label': sprint['name'],
                'status': sprint['status']
            }
            sprints_filter.append(sprint_option)
        
        filters['sprint'] = {
            'label': 'Sprint',
            'value': 'sprint',
            'options': sprints_filter
        }

    if args['members'] or args['epics']:
        team = Team.get_team(g.team_id)
 
    if args['members']:
        members = team['members']
        for member in members:
            member_option = {
                'key': member['_id']['$oid'],
                'label': member['username'] + (' (You)' if member['_id']['$oid'] == g._id else ''),
                'username': member['username'],
                'profile_picture': member['profile_picture'],
                'email': member['email'],
            }     
            members_filter.append(member_option)
        
        filters['assigned_to'] = {
            'label': 'Assigned to',
            'value': 'assigned_to',
            'options': members_filter
        }       

    if args['epics']:
        org_id = team["organization"]['$oid']
        epics = Epic.get_epics_from_organization(org_id)
        # print(epics)
        
        for epic in epics:
            epic_option = {
                'key': epic['_id']['$oid'],
                'label': epic['title'],
                'team': epic['team']
            }
            epics_filter.append(epic_option)
        
        filters['epic'] = {
            'label': 'Epic',
            'value': 'epic',
            'options': epics_filter
        }  

    if args['priority']:
        priority = [{'key': priority.value, 'label': priority.value} for priority in Priority]
        filters['priority'] = {
            'label': 'Priority',
            'value': 'priority',
            'options': priority
        }      

    if args['story_type']:
        story_type = [{'key': _type.value, 'label': _type.value} for _type in Type]
        filters['story_type'] = {
            'label': 'Story type',
            'value': 'story_type',
            'options': story_type
        } 

    if args['estimation']:
        estimation_methods = team['team_settings']['sprint_set_up']['estimation_method']
        try:
            estimation_methods.remove('planning_poker')
        except:
            pass
        estimation = Settings.get_estimation_method_options(estimation_methods[0])
        filters['estimation'] = {
            'label': estimation['label'],
            'value': 'estimation',
            'options': estimation['options']
        } 

    return send_response(filters, [], 200, **g.req_data)

@stories.route('/generate_id', methods=['GET'])
def generate_story_id():

    def generate_new_id():
        number = random.randint(1, 999999)
        complete_number = str(number).rjust(6, '0')
        team_name = Team.get_team(g.team_id)['name'].replace(" ", "_").upper()
        return team_name + "-" + complete_number
    
    story_id = generate_new_id()
    while Story.is_story_id_taken(story_id):
        story_id = generate_new_id()

    return send_response([story_id], [], 200, **g.req_data)

@stories.route('/create', methods=['POST'])
def create_story():
    story = request.json
    story['team'] = g.team_id

    tasks = Task.format(story)
    story['tasks'] = tasks

    try:
        response = Story.create_story(story)
        return send_response([response.acknowledged], [], 201, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to create story: {e}"], 500, **g.req_data)










# Validacion para la actualizacion de stories
# update_story_args = {
#     'title': fields.Str(required=False),
#     'description': fields.Str(required=False),
#     'acceptance_criteria': fields.Str(required=False),
#     'assigned_to': fields.List(fields.Str(), required=False),
#     'epic': fields.Str(required=False),
#     'sprint': fields.Int(required=False),
#     'story_points': fields.Int(required=False),
#     'tags': fields.List(fields.Str(), required=False),
#     'priority': fields.Str(required=False),
#     'estimation_method': fields.Str(required=False),
#     'type': fields.Str(required=False),
#     'tasks': fields.List(fields.Str(), required=False), 
#     'estimation': fields.Str(required=False),
#     'team': fields.Str(required=False)
# }
# @stories.route('/<string:story_id>', methods=['PUT'])
# def update_story(story_id):
#     current_user = get_current_user(request)
#     if current_user is None:
#         return jsonify({"message": "Unauthorized"}), 401

#     try:
#         args = request.get_json()
#         print("Received data:", args)

#         story = mongo.db.stories.find_one({"_id": ObjectId(story_id)})
#         if story is None:
#             return jsonify({"message": "Story not found."}), 404

#         creator_id = story.get('creator', {}).get('_id', None)
#         if creator_id != current_user['sub']:
#             return jsonify({"message": "Unauthorized to update this story."}), 403

#         # Manejar la lista de usuarios asignados
#         assigned_to_user_ids = args.get('assigned_to', [])
#         assigned_to_users = []
#         for user_id in assigned_to_user_ids:
#             if ObjectId.is_valid(user_id):
#                 user_id = ObjectId(user_id)
#                 user = mongo.db.users.find_one({"_id": user_id})
#                 if user:
#                     assigned_to_users.append({
#                         "_id": user['_id'], 
#                         "username": user.get('username', 'Unknown'),
#                         "profile_picture": user.get('profile_picture', '')
#                     })
#                 else:
#                     return jsonify({"message": f"Assigned user with ID {user_id} not found."}), 404
#             else:
#                 return jsonify({"message": f"Invalid user ID {user_id}."}), 400
#         if not assigned_to_users:
#             # Si no hay usuarios asignados, asignar al creador
#             assigned_to_users = [{
#                 "_id": current_user['sub'],
#                 "username": current_user.get('username', 'Unknown'),
#                 "profile_picture": current_user.get('picture', '')
#             }]

#         # Obtener los datos completos de las tareas
#         tasks = []
#         for task_id in args.get('tasks', []):
#             print("Task ID:", task_id)
#             task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
#             if task:
#                 tasks.append({
#                     "title": task.get("title"),
#                     "description": task.get("description"),
#                     "app": task.get("app"),
#                     "status": task.get("status")
#                 })
#             else:
#                 return jsonify({"message": f"Task with ID {task_id} not found."}), 404

#         # Obtener los datos del epic
#         epic_id = args.get('epic')
#         if ObjectId.is_valid(epic_id):
#             epic_id = ObjectId(epic_id)
#             epic_data = mongo.db.epics.find_one({"_id": epic_id})
#             if epic_data:
#                 epic_info = {
#                     "_id": epic_data["_id"],  
#                     "title": epic_data.get("title")
#                 }
#             else:
#                 return jsonify({"message": f"Epic with ID {epic_id} not found."}), 404
#         else:
#             return jsonify({"message": f"Invalid epic ID {epic_id}."}), 400
        
#         # Obtener los datos del equipo
#         team_id = args.get('team')
#         if team_id and ObjectId.is_valid(team_id):
#             team_id = ObjectId(team_id)
#             team_data = mongo.db.teams.find_one({"_id": team_id})
#             if team_data:
#                 team_info = {
#                     "_id": team_data["_id"],  
#                     "name": team_data.get("name")
#                 }
#             else:
#                 return jsonify({"message": f"Team with ID {team_id} not found."}), 404
#         else:
#             team_info = None
        
#         # Filtra los campos que se deben actualizar
#         update_fields = {
#             **args,
#             'assigned_to': assigned_to_users,
#             'tasks': tasks,
#             'epic': epic_info,
#             'team': team_info
#         }

#         # Solo actualiza los campos sin cambiar el título
#         result = mongo.db.stories.update_one({"_id": ObjectId(story_id)}, {"$set": update_fields})
#         if result.matched_count == 0:
#             return jsonify({"message": "Story update failed."}), 500

#         # Recupera la historia actualizada
#         updated_story = mongo.db.stories.find_one({"_id": ObjectId(story_id)})
#         if updated_story:
#             updated_story = convert_objectid_to_str(updated_story)
#             return jsonify(updated_story), 200
#         else:
#             return jsonify({"message": "Story update failed."}), 500

#     except Exception as e:
#         print(f"Exception: {e}")
#         return jsonify({"error": str(e)}), 500
