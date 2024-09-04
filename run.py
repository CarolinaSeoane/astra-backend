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
    '''
    This validation runs before any request made to any route except the excluded_routes or OPTIONS requests
    '''
    for route in excluded_routes:
        if request.path.startswith(route) or request.method=='OPTIONS':
            return None
    
    req_data = {
        'method': request.method,
        'endpoint': request.path,
    }

    token = request.headers.get('Authorization')

    if not token:
        return send_response([], [f"Unprocessable Entity. Missing Authorization header"], 422, **req_data)

    # Validate token
    decoded = validate_jwt(token)   
    if not decoded:
        return send_response([], [f"Unauthorized. Invalid session token"], 401, **req_data)
    
    g._id = decoded['_id']
    g.email = decoded['email']
    g.req_data = {
        'method': request.method,
        'endpoint': request.path,
    }