import requests
import json
import datetime


class ZohoMeetingAPI:
    
    def __init__(self, client_id, client_secret, access_token, refresh_token):

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.renew_access_token(refresh_token, client_id, client_secret)

    # this function is used to get the ZSOID keys, to be by the user to interact 
    def get_user_info(self):
        get_user_info_url = "https://meeting.zoho.in/api/v2/user.json"
        headers = {
            'Authorization': f"Zoho-oauthtoken {self.access_token}",
            'Content-Type': 'application/json'
        }
        response = requests.get(get_user_info_url, headers=headers)
        parsed_response = response.json()
        return parsed_response



    #this function is used to renew the access token using the refresh token 
    def renew_access_token(self, refresh_token: str, client_id: str, client_secret: str):
        
        #check if current access token has expired
        check_token_expiration_url = "https://meeting.zoho.in/api/v2/user.json" 
        headers_for_verification = {
            'Authorization': f"Zoho-oauthtoken {self.access_token}",
            'Content-Type': 'application/json'
        }
        verification_response = requests.request("GET", check_token_expiration_url, headers=headers_for_verification)
        print(verification_response.text) 

        if(verification_response.status_code != 200):
            # if has expired, regenerate with refresh token 
            renew_access_token_url = f"https://accounts.zoho.in/oauth/v2/token?refresh_token={self.refresh_token}&client_id={self.client_id}&client_secret={self.client_secret}&redirect_uri=http://43.204.149.165:8000/&grant_type=refresh_token"

            headers = {
                'Content-Type': 'application/json'
            }
            
            new_access_token_response = requests.post(renew_access_token_url, headers=headers)
            print(new_access_token_response)
            print(new_access_token_response.status_code)

            if(new_access_token_response.status_code == 200):
                response_data = new_access_token_response.json()
                print(response_data.get("access_token"))
                self.access_token = response_data.get("access_token") #to fix
                user_info_response = self.get_user_info()
                self.zsoid = user_info_response['userDetails']['zsoid']
                self.user_name = user_info_response['userDetails']['fullName']
                self.zuid = user_info_response['userDetails']['zuid']
                print(f"The current user is {self.user_name} and preseter id is {self.zuid}")
            else: 
                print("Can't renew access token")
        
        #else continue to use the same access token             
        else: 
            print("The access token is not expired yet")
            user_info_response = self.get_user_info()
            self.zsoid = user_info_response['userDetails']['zsoid']
            self.user_name = user_info_response['userDetails']['fullName']
            self.zuid = user_info_response['userDetails']['zuid']
            print(f"The current user is {self.user_name}")
            print(f"The current user's zsoid is {self.zsoid}")
            print(f"The current user's zuid is {self.zuid}")
          
   
    
     #this function is used to create the meeting
    def scheduleMeeting(self, topic: str, startTime: str,timezone: str, presenterId: int , duration: Union[int, None] = None, participants:list = None):
        print(self.access_token)
        request_url = f"https://meeting.zoho.in/api/v2/{self.zsoid}/sessions.json"
        print(f"Inside scheduleMeetng function")
        presenterId = self.zuid
        print(presenterId)
        payload = json.dumps(
        {
            "session": 
            {
                "topic": topic,
                "startTime": startTime,
                "presenter": presenterId,
                "timezone": timezone,
                "participants": participants
                # "participants": [
                # # []
                # {
                #     # "email": "mangesh.singh@codenia.in",
                #     "email": "radhika.kakkar@corewebconnections.com",
                # }
                # ] 
            }
        })

        headers = {
            'Authorization': f"Zoho-oauthtoken {self.access_token}",
            'Content-Type': 'application/json;charset=UTF-8',
        }
        try:
            response = requests.post(request_url, headers=headers, data=payload)

            if response.status_code == 200:
                parsed_response = response.text
                print(f"schedule meeting response: {parsed_response}")
                return parsed_response
            else: 
                parsed_response = response.text
                print(response)
                print(f"Failed to schedule meeting. Status code: {response.status_code}, Content: {parsed_response}")
                parsed_response_json = json.loads(parsed_response)
                return parsed_response
        except Exception as e:
            print(f"Exception in scheduling meeting: {e}")
            return None
    
     #this function is used to edit/update the meeting details
    def update_meeting(self, meetingKey: int, topic: str = None, agenda: str = None, presenterId: int = None, startTime: str =  None, duration: int = None, timezone: str = None, participants: str = None):
        request_url = f"https://meeting.zoho.in/api/v2/{self.zsoid}/sessions/{meetingKey}.json"
        presenterId = self.zuid
        headers = {
            'Authorization': f"Zoho-oauthtoken {self.access_token}",
            'Content-Type': 'application/json;charset=UTF-8'
        }
        session_payload = {
        "session": {}
        }   
    
        if topic is not None:
            session_payload["session"]["topic"] = topic
        if agenda is not None:
            session_payload["session"]["agenda"] = agenda
        if presenterId is not None:
            session_payload["session"]["presenter"] = presenterId
        if startTime is not None:
            session_payload["session"]["startTime"] = startTime
        if duration is not None:
            session_payload["session"]["duration"] = duration
        if timezone is not None:
            session_payload["session"]["timezone"] = timezone
        if participants is not None:
            session_payload["session"]["participants"] = [{"email":participants}]


        try: 
            payload_json = json.dumps(session_payload)
            print(payload_json)
            # print(headers)
            response = requests.request("PUT", request_url, headers=headers, data=payload_json)
            if response.status_code == 200:
                parsed_response = response.json()
                print(f"UPDATE meeting response: Status code: {response.status_code}, Content: {parsed_response}")
                return response
            else:
                print(f"Failed to UPDATE meeting. Status code: {response.status_code}")
                return response
            
        except Exception as e:
            print(f"Exception in UPDATING meeting: {e}")
            return None, 500

     #this function is used to fetch the details of the meeting
    def get_meeting_details(self, meetingKey: int):
        
        request_url = f"https://meeting.zoho.in/api/v2/{self.zsoid}/sessions/{meetingKey}.json"
        headers = {
            'Authorization': f"Zoho-oauthtoken {self.access_token}",
            'Content-Type': 'application/json;charset=UTF-8'
        }
        try: 
            response = requests.get(request_url, headers=headers)
            if response.status_code == 200:
                parsed_response = response.json()
                print(f"I'm get meeting details and my response is  - {parsed_response}")
                return response
            else:
                parsed_response = response.json()
                json_response = json.dumps(parsed_response)
                print(f"Failed to GET MEETING DETAILS meeting. Status code: {response.status_code}, Content: {response.text}")
                return Response(json_response, status=response.status_code) #to fix the status code here 
        except Exception as e:
            print(f"Exception in GET MEETING DETAILS meeting: {e}")
            return None
    
    #this function is used delete the meeting
    def delete_meeting(self, meetingKey: int):
        request_url = f"https://meeting.zoho.in/api/v2/{self.zsoid}/sessions/{meetingKey}.json"
        headers = {
            'Authorization': f"Zoho-oauthtoken {self.access_token}",
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = requests.delete(request_url, headers=headers)
        print(response.status_code)
        if response.status_code == 204:
            print("Meeting deleted")
            return response
        else:
            parsed_response = response.json()
            print(f"Failed to DELETE meeting. Status code: {response.status_code}, Content: {parsed_response}")
            return response
    
     #this function is used to get the recording data of the meeting
    def get_meeting_recording_url(self, meeting_key: str):
       
        url = f"https://meeting.zoho.in/meeting/api/v2/{self.zsoid}/recordings/{meeting_key}.json"
        headers = {
                'Authorization': f"Zoho-oauthtoken {self.access_token}",
                'Content-Type': 'application/json'
            }
        response = requests.get(url, headers=headers)
        parsed_response = response.json()
        try:
            play_url = parsed_response["recordings"][0]["playUrl"]
            return play_url
        except:
            return ""
   

    #custom functions 
    def has_meeting_ended(self, meetingKey: str, endTime: str, currentTime: datetime):
        # Convert the provided end time to a datetime object
        provided_date_time = datetime.strptime(endTime, "%b %d, %Y %I:%M %p")
        provided_date_time_aware = provided_date_time.replace(tzinfo=pytz.timezone('Asia/Kolkata'))
        
        print(f"Inside hasMeetingended function {provided_date_time} and {currentTime}")
        # Compare the two datetime objects
        if currentTime <= provided_date_time_aware:
            print("The meeting has not ended")
            return False
        else:
            print("The meeting has ended")
            return True
