import jwt
from datetime import datetime, timedelta, UTC
import os

JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')

def generate_jwt(user_email):
    payload = {
        'email': user_email,
        'exp': datetime.now(UTC) + timedelta(days=1)  # Expires in 1 day
    }
    token = jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)
    return token

# def validate_jwt(token):
#     try:
#         decoded = jwt.decode(token, SECRET_KEY, JWT_ALGORITHM)
#         return decoded
#     except jwt.ExpiredSignatureError:
#         return None  # Token has expired
#     except jwt.InvalidTokenError:
#         return None  # Invalid token
    