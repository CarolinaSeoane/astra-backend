from flask import jsonify


def send_response(method, endpoint, data, errors, status_code):  
    payload = {
        'meta': {
            'method': method,
            'endpoint': endpoint
        },
        'data': data,
        'errors': errors
    }
    return jsonify(payload), status_code
