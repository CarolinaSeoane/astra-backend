from flask import Blueprint, g, request
from webargs.flaskparser import use_args
from webargs import fields
import datetime

from app.models.story import Story
from app.utils import send_response, get_current_quarter
from app.routes.utils import validate_user_is_member_of_team
from app.models.team import Team
from app.models.sprint import Sprint


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
    }, location='query')
def stories_list(args, view_type):
    stories = Story.get_stories_by_team_id(g.team_id, view_type, **args)
    
    return send_response(stories, [], 200, **g.req_data)

@stories.route("/fields", methods=['GET'])
def story_fields():
    fields = Story.get_story_fields()
    return send_response(fields, [], 200, **g.req_data)

@stories.route("/filters", methods=['GET'])
@use_args({
    'quarter': fields.Str(required=False, missing=str(get_current_quarter(datetime.datetime.today()))),
    'year': fields.Str(required=False, missing=str(datetime.datetime.today().year)),
    }, location='query')
def filters(args):  
    sprints = Sprint.get_sprints(g.team_id, args['quarter'], args['year'])
    members = Team.get_team_members(g.team_id)

    sprints_filter = []
    for sprint in sprints:
        sprint_option = {
            'key': sprint['_id']['$oid'],
            'label': sprint['name'],
            'status': sprint['status']
        }
        sprints_filter.append(sprint_option)
    
    members_filter = []
    for member in members:
        member_option = {
            'key': member['_id']['$oid'],
            'label': member['username'] + (' (You)' if member['_id']['$oid'] == g._id else '')
        }
        members_filter.append(member_option)

    filters = {
        'sprint': {
            'label': 'Sprint',
            'options': sprints_filter
        },
        'assigned_to': {
            'label': 'Assigned to',
            'options': members_filter
        }
    }
    return send_response(filters, [], 200, **g.req_data)

