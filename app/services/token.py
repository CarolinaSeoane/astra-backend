import os
from datetime import datetime, timedelta, UTC
import jwt


JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')

def generate_jwt(user_email, _id):
    payload = {
        'email': user_email,
        '_id': _id,
        'exp': datetime.now(UTC) + timedelta(days=1)  # Expires in 1 day
    }
    token = jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)
    return token

def validate_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, JWT_ALGORITHM)
        return decoded
    except Exception: # Token has expired or is invalid
        return None
