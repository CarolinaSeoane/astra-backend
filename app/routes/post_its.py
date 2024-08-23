from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from app.models.post_it import PostIt
from app.db_connection import mongo
from app.routes.utils import validate_user_is_member_of_team  

post_its = Blueprint("post_its", __name__)

# Rutas excluidas de la validación de usuario
excluded_routes = []

@post_its.before_request
def apply_validate_user_is_member_of_team():
    if any(request.path.startswith(route) for route in excluded_routes):
        return None
    return validate_user_is_member_of_team()

@post_its.route("/", methods=['GET'])
@use_args({'sprint_id': fields.Str(required=True)}, location='query')
def get_post_its(args):
    sprint_id = args.get('sprint_id')
    
    # Verifica si el sprint_id es válido
    if not sprint_id:
        return jsonify({"error": "sprint_id is required"}), 400
    
    # Consulta de post-its por sprint_id
    post_its_cursor = mongo.db.post_its.find({"sprint_id": sprint_id})
    post_its = list(post_its_cursor)
    
    # Transforma el ObjectId en string
    for post_it in post_its:
        post_it['_id'] = str(post_it['_id'])
    
    return jsonify(post_its)

@post_its.route("/", methods=['POST'])
@use_args({'content': fields.Str(required=True), 'sprint_id': fields.Str(required=True)}, location='json')
def add_post_it(args):
    content = args.get('content')
    sprint_id = args.get('sprint_id')
    
    print("contenido a guardar:" +  content)
    print("print_id: " + sprint_id)

    # Validación de datos
    if not content or not sprint_id:
        return jsonify({"error": "Both content and sprint_id are required"}), 400
    
    new_post_it = PostIt(content=content, sprint_id=sprint_id)
    print("antes del try")
    # Inserción de nuevo post-it
    try:        
        # Convertimos el objeto PostIt a un diccionario
        post_it_dict = new_post_it.to_dict()
        result = mongo.db.post_its.insert_one(post_it_dict)
        post_it_dict['_id'] = str(result.inserted_id)  # Asignamos el _id al diccionario
        print("guardado exitoso")
        return jsonify(post_it_dict), 201  # Retornamos el diccionario
    except Exception as e:
        print("Ocurrió una excepción:", str(e))  # Debugging: Ver el error exacto
        # Manejo de errores en la base de datos
        return jsonify({"error": str(e)}), 500
