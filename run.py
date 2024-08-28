from flask import request, g
from flask_socketio import SocketIO
from app.services.token import validate_jwt
from app.utils import send_response
from flask_cors import CORS
from app import create_app
from socketio_manager import socketio
app = create_app()

# Initialize SocketIO
socketio.init_app(app)

CORS(app)
# Define your SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('update_postit')
def handle_update_postit(data):
    #socketio.emit('postit_updated', data, broadcast=True)
    socketio.emit('postit_updated', data)
@socketio.on('delete_postit')
def handle_delete_postit(data):
    #socketio.emit('postit_deleted', data, broadcast=True)
    socketio.emit('postit_deleted', data)
@socketio.on('add_postit')
def handle_add_postit(data):
    #socketio.emit('postit_added', data, broadcast=True)
    socketio.emit('postit_added', data)
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
