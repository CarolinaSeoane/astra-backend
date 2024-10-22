import random
from datetime import datetime
from flask import Blueprint, g, request,jsonify
from webargs.flaskparser import use_args
from webargs import fields
from bson import ObjectId

from app.models.story import Story
from app.utils import send_response
from app.routes.utils import validate_user_is_active_member_of_team
from app.models.team import Team
from app.models.sprint import Sprint
from app.models.epic import Epic
from app.models.task import Task
from app.models.user import User
from app.services.mongoHelper import MongoHelper
from app.models.configurations import Priority, Type, Configurations, Status
from app.services.astra_scheduler import get_quarter


stories = Blueprint("stories", __name__)

excluded_routes = [
    '/stories/fields'
]

DOING = Status.DOING.value


@stories.before_request
def apply_validate_user_is_active_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None
    return validate_user_is_active_member_of_team()

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
    'task_statuses': fields.Boolean(required=False, missing=True),
    ## customization
    'quarter': fields.Integer(required=False, missing=get_quarter(datetime.today())), # affects sprints (TODO: should affect epics too!!!!)
    'year': fields.Integer(required=False, missing=datetime.today().year), # affects sprints (TODO: should affect epics too!!!!)
    'future': fields.Str(required=False, missing=False), # affects sprints (TODO: should affect epics too!!!!)
    }, location='query')
def filters(args):
    sprints_filter = []
    members_filter = []
    epics_filter = []
    priority = []
    story_type = []
    estimation = []
    task_statuses = []
    filters = {}

    if args['sprints']:
        sprints = Sprint.get_sprints(g.team_id, args['quarter'], args['year'], args['future'])

        if sprints:
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
        if members:
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
        if team["organization"]:
            org_id = team["organization"]['$oid']
            epics = Epic.get_epics_from_organization(org_id)
        else:
            epics = Epic.get_epics_from_team(g.team_id)

        if epics:
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
        estimation_methods = team['estimation_method']
        try:
            estimation_methods.remove('planning_poker')
        except Exception:
            pass

        est_method = estimation_methods[0]
        estimation = Configurations.get_estimation_method_options(est_method)

        filters['estimation'] = {
            'label': estimation[est_method]['label'],
            'value': 'estimation',
            'options': estimation[est_method]['options']
        }

    if args['task_statuses']:
        statuses = Task.get_statuses()
        for status in statuses:
            task_statuses.append({
                "label": status,
                "key": status
            })
        filters['task_statuses'] = task_statuses

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
    story['story_status'] = Status.NOT_STARTED.value

    try:
        response = Story.create_story(story)
        
        return send_response([response.acknowledged], [], 201, **g.req_data)
    except Exception as e:
        print(f"Error en create_story: {e}")
        return send_response([], [f"Failed to create story: {e}"], 500, **g.req_data)

@stories.route('/view', methods=['GET'])
@use_args({"story_id": fields.Str(required=True)}, location="query")
def retrieve_story(args):
    story = Story.get_story_by_id(args["story_id"])
    return send_response(story, [], 200, **g.req_data)

@stories.route('/edit', methods=['PUT'])
def edit_story():
    # if the story goes into doing, we need to include a start_date
    # if the story goes into done, we need to include an end_date
    # if the sprint is modified, we need to update the added_to_sprint value
    story = request.json
    story['team'] = g.team_id
    date_now = datetime.combine(datetime.now().date(), datetime.min.time())
    old_story = Story.get_story_by_id(story["story_id"])
    print(f"Received story for editing: {old_story}")
    user = get_current_user() 
    username = user["username"]
    modified_story_info = {
        "story_id": story["story_id"],
        "title": story["title"],

        "modified_by": username,
        "modified_at": datetime.now().date().isoformat(),
        "sprint": story["sprint"]["name"],
        "team_id":story['team']
    }
    if "_id" in story:
        del story["_id"]
    if old_story["sprint"]["name"] != story["sprint"]["name"]:
        story["added_to_sprint"] = date_now

    tasks = Task.format(story)
    story["tasks"] = tasks
    if Story.is_done(story):
        try:
            
            response = Story.finalize_story(story, g.team_id)

            return send_response([response.acknowledged], [], 201, **g.req_data)
        except Exception as e:
            return send_response([], [f"Failed to update story: {e}"], 500, **g.req_data)

    story_status = Task.get_story_status(story["tasks"])
    if story_status == DOING and "start_date" not in story:
        story["start_date"] = date_now
        print(f"Start date added: {date_now}")
    try:
        response = Story.update(story, story_status)
        save_modified_story(
                modified_story_info["story_id"],
                modified_story_info["title"],
                modified_story_info["modified_by"],
                modified_story_info["modified_at"],
                modified_story_info["sprint"],
                modified_story_info["team_id"],
            )
        return send_response([response.acknowledged], [], 201, **g.req_data)
    except Exception as e:
        print(f"Error updating story: {e}")
        return send_response([], [f"Failed to update story: {e}"], 500, **g.req_data)

@stories.route('/delete', methods=['DELETE'])
@use_args({"story_id": fields.Str(required=True)}, location="query")
def delete_story(args):
    mongo_helper = MongoHelper()
    try:
        Story.delete(g.team_id, args["story_id"])
        result = mongo_helper.delete_many("modified_stories", {
            "team_id": g.team_id,
            "story_id": args["story_id"]
        })

        print(f"Modified stories deleted: {result.deleted_count}")
        return send_response([], [], 204, **g.req_data)
    except Exception as e:
        print(f"error deleting story: {e}")
        return send_response([], [], 500, **g.req_data)

@stories.route('/modified_stories', methods=['GET'])
def get_modified_stories():
    mongo_helper = MongoHelper()
    team_id = request.args.get('team_id')
    sprint_id = request.args.get('sprint')
    
    print(f"Received team_id: {team_id}, sprint: {sprint_id}")

    filter_query = {'team_id': ObjectId(team_id)}

    if sprint_id:
        filter_query['sprint'] = sprint_id
        
    modified_stories = mongo_helper.get_documents_by('modified_stories', filter_query)
    print(f"Filter query: {filter_query}")
    print(f"Modified stories found: {modified_stories}")

    return jsonify(modified_stories)

def save_modified_story(story_id, title, username, modified_at,sprint,team_id):
    mongo_helper = MongoHelper()
    modified_story = {
        "story_id": story_id,
        "title": title,
        "username": username,
        "modified_at": modified_at,
        "sprint": sprint,
        "team_id": team_id
    }
    print(f"Saving modified story: {modified_story}") 
    result = mongo_helper.create_document('modified_stories', modified_story)
    print(f"Result of save: {result}")

def get_current_user():
    user_id = g._id  
    if user_id:
        user = User.get_user_by({"_id": ObjectId(user_id)})
        return user
    else:
        return None
    
@stories.route('/backlog', methods=['GET'])
@use_args({'team_id': fields.Str(required=True), 'sprint': fields.Str(required=False)}, location='query')
def get_backlog(args):
    team_id = args.get('team_id')
    #sprint =  args.get('sprint')
    #team_id = args['team_id']  # Extraer team_id de los argumentos
    #sprint = args['sprint'] 
    try:
        stories = Story.get_backlog_stories(team_id)  # Llamar a la función mejorada
        #print("stories", stories)
        return send_response(stories, [], 200, **g.req_data)  # Retornar historias
    except Exception as e:
        print(f"Error retrieving backlog stories: {e}")
        return send_response([], [f"Failed to retrieve backlog storiess: {e}"], 200, **g.req_data)


#convine list with story status that doesnot exist in stories/<view>
@stories.route('/list_with_story_status', methods=['GET'])
@use_args({'team_id': fields.Str(required=True), 'sprint': fields.Str(required=True)}, location='query')
def list_with_story_status(args):
    team_id = args.get('team_id')
    sprint =  args.get('sprint')

    #print("    team_id",team_id )
    
    #print("    sprint ", sprint)
    #team_id = args['team_id']  # Extraer team_id de los argumentos
    #sprint = args['sprint'] 
    try:
        stories = Story.get_list_stories_by_team_id_with_story_status(team_id, sprint)  # Llamar a la función mejorada
        #print("stories", stories)
        return send_response(stories, [], 200, **g.req_data)  # Retornar historias
    except Exception as e:
        #print(f"Error retrieving backlog stories: {e}")
        return send_response([], [f"Failed to retrieve backlog stories: {e}"], 200, **g.req_data)