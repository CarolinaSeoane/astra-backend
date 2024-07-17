from google.oauth2 import id_token
from google.auth.transport import requests
import os

CLIENT_ID = os.getenv('CLIENT_ID')

def validate_credentials(user_token):
    # Specify the CLIENT_ID of the app that accesses the backend:
    id_info = id_token.verify_oauth2_token(user_token, requests.Request(), CLIENT_ID)
    
    # The verify_oauth2_token function verifies the JWT signature,
    # the aud claim, and the exp claim. You must also verify the hd
    # claim (if applicable) by examining the object that verify_oauth2_token
    # returns. If multiple clients access the backend server, also manually
    # verify the aud claim.
    
    # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    # If the request specified a Google Workspace domain
    # if idinfo['hd'] != DOMAIN_NAME:
    #     raise ValueError('Wrong domain name.')

    return id_info
