import requests
import datetime
from datetime import timezone


class ZohoAuth:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        self.client_id = config.get('zoho_client_id')
        self.client_secret = config.get('zoho_client_secret')
        self.redirect_uri = config.get('redirect_uri')


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
    
    def get_access_token(self, auth_grant):
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
            zoho_access_token_created_time = datetime.now()
            return response.json()['access_token'], response.json()['refresh_token']
        else:
            pass

    def renew_access_token(self, refresh_token):
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
            zoho_access_token_created_time = datetime.now()
            return response_data.get('access_token')
        
        else:
            pass

    def generate_zoho_tokens(self):

        auth_grant = self.get_auth_grant()
        zoho_access_token, zoho_refresh_token = self.get_access_token(auth_grant)
        current_time = datetime.now(timezone.utc)
        time_difference = current_time - zoho_access_token_created_time
        if time_difference.total_seconds() > 3600:
            zoho_access_token = self.renew_access_token(zoho_access_token)

        return {
            "access_token": zoho_access_token,
            "refresh_token": zoho_refresh_token
        }

