import os
import requests


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def call_google_api(url, method, user_tokens):
    print('user_tokens: ', user_tokens)
    headers = {
        'Authorization': f'Bearer {user_tokens["google_access_token"]}',
        'Content-Type': 'application/json'
    }

    response = getattr(requests, method)(url, headers=headers)

    if response.status_code == 401:
        print("Access token expired, refreshing token...")
        # Refresh the access token
        google_access_token = refresh_access_token(user_tokens['refresh_token'])
        # Retry the request with the new access token
        headers['Authorization'] = f'Bearer {google_access_token}'
        response = requests.post(url, headers=headers)

    # Handle success or error in the retried request
    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print('An error occurred while using Google Meet API')
        raise RuntimeError

def create_space(google_access_token, refresh_token):
    url = 'https://meet.googleapis.com/v2/spaces'

    # Send token as auth header
    headers = {
        'Authorization': f'Bearer {google_access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers)

    # Check if the token is expired (Google typically returns a 401)
    if response.status_code == 401:
        print("Access token expired, refreshing token...")
        # Refresh the access token
        google_access_token = refresh_access_token(refresh_token)
        # Retry the request with the new access token
        headers['Authorization'] = f'Bearer {google_access_token}'
        response = requests.post(url, headers=headers)

    # Handle success or error in the retried request
    if response.status_code == 200:
        return response.json()
    else:
        print('An error occurred when creating a Google Meet space')
        print(response.text)
        raise RuntimeError

def refresh_access_token(refresh_token):
    url = "https://oauth2.googleapis.com/token"

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        # Extract the new access token from the response
        return response.json()['access_token']
    else:
        print("Failed to refresh access token")
        print(response.text)
        raise RuntimeError("Could not refresh access token")

def list_conference_records(google_access_token, refresh_token, ceremony):
    url = 'https://meet.googleapis.com/v2/conferenceRecords'
    query_params = '?filter=space.meeting_code="' + ceremony['google_meet_config']['meetingCode'] + '"'

    return call_google_api(url + query_params, 'get', {'google_access_token': google_access_token, 'refresh_token': refresh_token})
    