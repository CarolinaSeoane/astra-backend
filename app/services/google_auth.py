import os
import requests


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def exchange_code_for_tokens(auth_code):
    
    url = 'https://oauth2.googleapis.com/token'

    data = {
        'code': auth_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:3000',  # Matches Google Cloud Console set up
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data=data)
    
    tokens = response.json()
    print(tokens)

    return tokens

def validate_credentials(google_access_token):
    # Get user information from Google API
    url = 'https://www.googleapis.com/oauth2/v2/userinfo'

    # Send token as auth header
    headers = {
        'Authorization': f'Bearer {google_access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError

