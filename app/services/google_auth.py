import os
import requests

CLIENT_ID = os.getenv('CLIENT_ID')

def validate_credentials(google_access_token):
    # Get user information from Google API
    url = 'https://www.googleapis.com/oauth2/v2/userinfo'

    # Send token as auth header
    headers = {
        'Authorization': f'Bearer {google_access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
  
    # url = 'https://meet.googleapis.com/v2/spaces'   PRUEBA DE CREAR UN MEETING SPACE CON EL ACCESS TOKEN. VERIFICAR REFRESH TOKEN
    # response_2 = requests.post(url, headers=headers, data={})
    # print(response_2.text, response_2.content)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError

