import requests
import datetime
from datetime import datetime, timezone, timedelta
from app.config.config import ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, REDIRECT_URI
import json
import os
from urllib.parse import urlparse, parse_qs

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


    # def get_auth_grant(self):
    #     if not self.client_secret or not self.client_id or not self.redirect_uri:
    #         return None
    #     params = {
    #         'scope': 'ZohoMeeting.meeting.UPDATE,ZohoMeeting.meeting.READ,ZohoMeeting.meeting.CREATE,ZohoMeeting.meeting.DELETE,ZohoMeeting.recording.READ',
    #         'client_id': self.client_id,
    #         'response_type': 'code',
    #         'access_type': 'offline',
    #         'redirect_uri': self.redirect_uri,
    #         'prompt': 'consent'
    #     }
    #     url = f'https://accounts.zoho.in/oauth/v2/' + 'auth'
    #     response = requests.get(url, params=params, headers=self.headers)
    #     url = response.url
    #     print(response.url)
    #     parsed_url = urlparse(url)
    #     query_params = parse_qs(parsed_url.query)
    #     code_value = query_params.get('code', [None])[0]
    #     print(f"the response from get_auth_grant is {code_value}")
    #     return code_value
    

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

           # This functions validates the access token and returns a new one in case there is none present 
    def get_access_token(self, auth_grant):
        token: str = ""
        try: 
            if os.path.exists(self.__token_file):
                with open(self.__token_file, "r") as read_file:
                    file_content_json = json.load(read_file)
                    token = file_content_json["access_token"]
                    refresh_token = file_content_json["refresh_token"]
                    created_at = datetime.strptime(file_content_json['created_at'], "%Y-%m-%d %H:%M:%S.%f")
                if datetime.now() - created_at >= timedelta(seconds=3600):
                    token = self.renew_access_token(refresh_token)

            elif not os.path.exists(self.__token_file):
                print("inside elif")
                params = {
                    'code': auth_grant,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'redirect_uri': self.redirect_uri,
                    'grant_type': 'authorization_code',
                    'prompt': 'consent'
                }
                url = f'https://accounts.zoho.in/oauth/v2/' + 'token'
                response = requests.post(url, params=params, headers=self.headers)
                print(response.status_code)
                parsed_response = response.json()

                if not response.status_code == 200:
                    print("the status code is not 200")

                token = parsed_response["access_token"]
                refresh_token = parsed_response["refresh_token"]
                file_content_json = {
                    "access_token": token,
                    "refresh_token": refresh_token,
                    "created_at": str(datetime.now())
                }
                with open(self.__token_file, "w") as file:
                    json.dump(file_content_json, file, indent=4)
        except Exception as e:
            print(f"exception is {e}")
        finally: 
            return token 
   

    def get_or_generate_zoho_token(self):

        # auth_grant = self.get_auth_grant()
        zoho_access_token = self.get_access_token("1000.acc92e0f3a9add8ecf5269229e32a67a.b3f64993d54f6921469a679a0b501957")
        return {
            "access_token": zoho_access_token,
        }

