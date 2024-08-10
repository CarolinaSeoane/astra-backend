from flask import request, g

from app.services.token import validate_jwt
from app.utils import send_response

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


excluded_routes = [
    '/users',
    '/astra',
]

@app.before_request
def validate_user_token():
   # if not request.headers.get('Authorization'):
   #     return send_response([], ["Unprocessable Entity. Missing Authorization header"], 422, method='GET', endpoint='/epics')
    # Excluir rutas específicas y métodos OPTIONS
    if any(request.path.startswith(route) for route in excluded_routes) or request.method == 'OPTIONS':
        return None

    # Verificar encabezado de autorización
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return send_response([], ["Unprocessable Entity. Missing Authorization header"], 422, method=request.method, endpoint=request.path)
    

    for route in excluded_routes:
        if request.path.startswith(route) or request.method=='OPTIONS':
            return None
    
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    #token = request.headers.get('Authorization')
    #if token:
    #    token = token.replace('Bearer ', '')  # Elimina "Bearer " si está incluido
    #else:
    #    return send_response([], [f"Unprocessable Entity. Missing Authorization header"], 422)
        # Procesar el token
    token = auth_header.replace('Bearer ', '')
    if not token:
        return send_response([], [f"Unprocessable Entity. Missing Authorization header"], 422, **req_data)

    #Validate token
    
    decoded = validate_jwt(token)   
    if 'error' in decoded:
        return send_response([], [f"Unauthorized. {decoded['error']}"], 401, **req_data)
    
    if '_id' not in decoded:
        return send_response([], ["Unauthorized. Token missing '_id'"], 401, **req_data)
    
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)
    
    g._id = decoded['_id']
    g.email = decoded['email']
    g.req_data = {
        'method': request.method,
        'endpoint': request.path,
    }
