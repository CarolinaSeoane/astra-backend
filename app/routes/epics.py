from flask import Blueprint, request, g

from app.utils import send_response
from app.models.epic import Epic
from app.routes.utils import validate_user_is_member_of_team


epics = Blueprint('epics', __name__)

excluded_routes = []

@epics.before_request
def apply_validate_user_is_member_of_team():
    for excluded_route in excluded_routes:
        if request.path.startswith(excluded_route['route']) and (request.method in excluded_route['methods']):
            return None

    return validate_user_is_member_of_team()

@epics.route('/create', methods=['POST'])
def create_story():
    epic = request.json
    epic['team'] = g.team_id

    try:
        response = Epic.create_epic(epic)
        return send_response([response], [], 201, **g.req_data)
    except Exception as e:
        return send_response([], [f"Failed to create epic: {e}"], 500, **g.req_data)



# Validación para la actualización de epics
# update_epic_args = {
#     'description': fields.Str(required=False),
#     'sprints': fields.Str(required=False),
#     'priority': fields.Str(required=False),
# }

# @epics.route('/<string:title>', methods=['PUT'])
# def update_epic(title):
#     current_user = get_current_user(request)
#     if current_user is None:
#         return jsonify({"message": "Unauthorized"}), 401

#     try:
#         args = request.get_json()
        
#         epic = mongo.db.epics.find_one({"title": title})
#         if not epic:
#             return jsonify({"message": "Epic not found."}), 404

#         creator_id = epic.get('creator', {}).get('_id', None)
#         if creator_id != current_user['sub']:
#             return jsonify({"message": "Unauthorized to update this epic."}), 403

#         update_fields = {key: value for key, value in args.items() if value is not None}

#         if update_fields:
#             result = mongo.db.epics.update_one({"title": title}, {"$set": update_fields})
#             if result.matched_count == 0:
#                 return jsonify({"message": "Epic update failed."}), 500

#         updated_epic = mongo.db.epics.find_one({"title": title})
#         if updated_epic:
#             updated_epic = convert_objectid_to_str(updated_epic)
#             return jsonify(updated_epic), 200
#         else:
#             return jsonify({"message": "Epic update failed."}), 500

#     except Exception as e:
#         print(f"Exception: {e}") 
#         return jsonify({"error": str(e)}), 500

# @epics.route('/', methods=['GET'])
# def get_all_epics():
#     current_user = get_current_user(request)
#     if current_user is None:
#         return jsonify({"message": "Unauthorized"}), 401
    
#     try:
#         epics_list = mongo.db.epics.find({"creator._id": current_user['sub']})
#         epics_data = [convert_objectid_to_str(epic) for epic in epics_list]
#         return jsonify(epics_data), 200
#     except Exception as e:
#         print(f"Exception: {e}")  
#         return jsonify({"error": str(e)}), 500
