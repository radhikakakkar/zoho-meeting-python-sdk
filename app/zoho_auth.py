import requests
import datetime
from datetime import timezone, timedelta
from app.config.config import ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, REDIRECT_URI
import json
import os

class ZohoAuth:
    def __init__(self):
        self.__token_file: str = ".token.json"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        self.client_id = ZOHO_CLIENT_ID
        self.client_secret = ZOHO_CLIENT_SECRET
        self.redirect_uri = REDIRECT_URI


    def get_auth_grant(self):
        if not self.client_secret or not self.client_id or not self.redirect_uri:
            return None
        params = {
            'scope': 'ZohoMeeting.manageOrg.READ,ZohoMeeting.meeting.UPDATE,ZohoMeeting.meeting.READ,ZohoMeeting.meeting.CREATE,ZohoMeeting.meeting.DELETE,ZohoMeeting.recording.READ',
            'client_id': self.client_id,
            'response_type': 'code',
            'access_type': 'offline',
            'redirect_uri': self.redirect_uri,
            'prompt': 'consent'
        }
        url = f'https://accounts.zoho.in/oauth/v2/' + 'auth'
        response = requests.get(url, params=params, headers=self.headers)
        return response.url
    
    # This functions validates the access token and returns a new one in case there is none present 
    def get_access_token(self, auth_grant):

        token: str

        try: 
            if os.path.exists(self.__token_file):
                with open(self.__token_file, "r") as read_file:
                    file_content_json = json.load(read_file)
                    token = file_content_json["access_token"]
                    created_at = datetime.strptime(file_content_json['created_at'], "%Y-%m-%d %H:%M:%S.%f")
                if datetime.now() - created_at >= timedelta(seconds=3600):
                    token = self.renew_access_token()

            elif not os.path.exists(self.__token_file):
                params = {
                    'code': auth_grant,
                    'client_id': self.client_id,
                    'client_secret': self.secret,
                    'redirect_uri': self.redirect_uri,
                    'grant_type': 'authorization_code',
                    'prompt': 'consent'
                }
                url = f'https://accounts.zoho.in/oauth/v2/' + 'token'
                response = requests.post(url, params=params, headers=self.headers)
                if response.status_code == 200 and response.json().get('access_token'):
                    token = response.json().get('access_token')
                    file_content_json: dict = {
                        "access_token": response.json().get('access_token'),
                        "created_at": str(datetime.now())
                    }
                    with open(self.__token_file, "w") as file:
                        json.dump(file_content_json)
                else:
                    pass
        except:
            pass
        finally: 
            return token 

    # this function return the new token if the previous one is expired or did not exist 
    def renew_access_token(self, refresh_token):

        token: str

        try:

            params = {
                'refresh_token': refresh_token,
                'client_id': self.client_id,
                'client_secret': self.secret,
                'redirect_uri': self.redirect_uri,
                'grant_type': 'refresh_token',
                'prompt': 'consent'
            }

            url = f'https://accounts.zoho.in/oauth/v2/' + 'token'
            response = requests.post(url, params=params, headers=self.headers)
            response_data = response.json()

            if response_data.get('access_token'):
                token = response_data.get('access_token')
                file_content: dict = {
                    "access_token": response_data.get('access_token'),
                    "created_at": str(datetime.now()) 
                }
                with open(self.__token_file, "w") as file: 
                    json.dump(file_content, file, indent=4)

        except:
            pass
        finally: 
            return token

          

    def get_or_generate_zoho_token(self):

        auth_grant = self.get_auth_grant()
        zoho_access_token = self.get_access_token(auth_grant)
        return {
            "access_token": zoho_access_token,
        }

