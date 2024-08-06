from flask import Blueprint, g, request

from app.models.story import Story
from app.utils import send_response
from app.routes.utils import validate_user_is_member_of_team


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
def stories_list(view_type): 
    stories = Story.get_stories_by_team_id(g.team_id, view_type)

    return send_response(stories, [], 200, **g.req_data)

@stories.route("/fields", methods=['GET'])
def story_fields():
    fields = Story.get_story_fields()
    return send_response(fields, [], 200, **g.req_data)

# @stories.route("/filters", methods=['GET'])
# def story_fields():
#     # fields = Story.get_story_fields()
#     return send_response(filters, [], 200, **g.req_data)
