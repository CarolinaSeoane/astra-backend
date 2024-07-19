from flask import jsonify


def send_response(data, errors, status_code, method, endpoint):  
    payload = {
        'meta': {
            'method': method,
            'endpoint': endpoint
        },
        'data': data,
        'errors': errors
    }
    return jsonify(payload), status_code
