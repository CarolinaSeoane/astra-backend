from flask import Blueprint, g, request, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from app.models.post_it import PostIt
from app.db_connection import mongo
from app.routes.utils import validate_user_is_member_of_team  

post_its = Blueprint("post_its", __name__)

excluded_routes = []

@post_its.before_request
def apply_validate_user_is_member_of_team():
    for route in excluded_routes:
        if request.path.startswith(route):
            return None

    return validate_user_is_member_of_team()

@post_its.route("/", methods=['GET'])
@use_args({'sprint_id': fields.Str(required=True)}, location='query')
def get_post_its(args):
    sprint_id = args.get('sprint_id')
    
    post_its = list(mongo.db.post_its.find({"sprint_id": sprint_id}))
    for post_it in post_its:
        post_it['_id'] = str(post_it['_id'])
    return jsonify(post_its)

@post_its.route("/", methods=['POST'])
@use_args({'content': fields.Str(required=True), 'sprint_id': fields.Str(required=True)}, location='json')
def add_post_it(args):
    new_post_it = PostIt(content=args['content'], sprint_id=args['sprint_id'])
    
    mongo.db.post_its.insert_one(new_post_it.to_dict())
    return jsonify(new_post_it.to_dict()), 201