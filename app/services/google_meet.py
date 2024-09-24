import requests


def create_space(google_access_token):
    # TODO: handle token refresh
    url = 'https://meet.googleapis.com/v2/spaces'

    # Send token as auth header
    headers = {
        'Authorization': f'Bearer {google_access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers)
      
    if response.status_code == 200:
        return response.json()
    else:
        print('An error occurred when creating a Google Meet space')
        print(response.text)
        raise RuntimeError