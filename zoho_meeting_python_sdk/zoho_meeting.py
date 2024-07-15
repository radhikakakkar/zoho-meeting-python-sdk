import requests
import json
import datetime
from typing import Union
import pytz
from datetime import timezone
from .zoho_auth import ZohoAuth

# the presented ID will be sent as an argument when an object is created and a function is called, as it should not be related to the class but that specific call to the object
# the access token for each user(presenter) should be different? - if so renew_access_token cannot be a class method


class ZohoMeetingAPI:
    # class variables

    def __init__(self):
        obj_auth = ZohoAuth()
        zoho_tokens: dict = obj_auth.get_or_generate_zoho_token()
        self.headers = {
            "Authorization": f"Zoho-oauthtoken {zoho_tokens['access_token']}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "cache-control": "no-cache",
        }

    #this function gets the details of the user 
    def __get_user_info(self):
        try:
            get_user_info_url = "https://meeting.zoho.in/api/v2/user.json"
            response = requests.get(get_user_info_url, headers=self.headers)
            parsed_response = response.json()
            return {
                "status": "success",
                "message": f"User details are: {parsed_response}",
                "data": parsed_response
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Exception occured in getting user details",
            }
    def __get_zsoid(self):
        response = self.__get_user_info()
        return response['data']['userDetails']['zsoid']
    
    def __get_zuid(self):
        response = self.__get_user_info()
        return response['data']['userDetails']['zuid']

    
        
    # this function is used to create the meeting
    def schedule_meeting(
        self,
        topic: str,
        startTime: str,
        timezone: str,
        presenterId: int = None,
        duration: Union[int, None] = None,
        participants: list = None,
    ):
        request_url = f"https://meeting.zoho.in/api/v2/{self.__get_zsoid()}/sessions.json"
        presenterId = self.__get_zuid()
        participants = [{"email": "radhika3273@gmail.com"}]
        payload = json.dumps(
            {
                "session": {
                    "topic": topic,
                    "startTime": startTime,
                    "presenter": presenterId,
                    "timezone": timezone,
                    "participants": participants,
                }
            }
        )

        try:
            response = requests.post(request_url, headers=self.headers, data=payload)
            if response.status_code == 200:
                json_response = response.json()
                return {
                    "status": "success",
                    "message": "Meeting Created!",
                    "data": json_response,
                }
            else:
                json_response = response.json()
                return {
                    "status": "error",
                    "message": "Meeting could not be Created :(",
                    "data": json_response,
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Exception in creating meeting : {e}",
            }

    # this function is used to edit/update the meeting details
    def update_meeting(
        self,
        meetingKey: int,
        topic: str = None,
        agenda: str = None,
        presenterId: int = None,
        startTime: str = None,
        duration: int = None,
        timezone: str = None,
        participants: str = None,
    ):
        request_url = (
            f"https://meeting.zoho.in/api/v2/{self.__get_zsoid()}/sessions/{meetingKey}.json"
        )
        presenterId = self.__get_zuid()
        session_payload = {"session": {}}

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
            session_payload["session"]["participants"] = [{"email": participants}]

        try:
            payload_json = json.dumps(session_payload)
            response = requests.request(
                "PUT", request_url, headers=self.headers, data=payload_json
            )
            if response.status_code == 200:
                parsed_response = response.json()
                return {"status": "success", "message": "Meeting updated"}
            else:
                return {"status": "error", "message": "Meeting could not be updated"}

        except Exception as e:
            return {
                "status": "error",
                "message": f"Exception occured in uodating meeting - {e}",
            }

    # this function is used to fetch the details of the meeting
    def get_meeting_details(self, meetingKey: int):

        request_url = (
            f"https://meeting.zoho.in/api/v2/{self.__get_zsoid()}/sessions/{meetingKey}.json"
        )
        try:
            response = requests.get(request_url, headers=self.headers)
            json_response = response.json()
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": f"The meeting details are {json_response}",
                }
            else:
                return {
                    "status": "error",
                    "message": "The meeting details could not be fetched",
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Exception occured in fetching meeting details : {e}",
            }

    # this function is used delete the meeting
    def delete_meeting(self, meetingKey: int):
        request_url = (
            f"https://meeting.zoho.in/api/v2/{self.__get_zsoid()}/sessions/{meetingKey}.json"
        )
        try:
            response = requests.delete(request_url, headers=self.headers)
            json_reponse = response.json()
            if response.status_code == 204:
                return {
                    "status": "success",
                    "message": "The meeting was successfully deleted",
                    "data": json_reponse,
                }
            else:
                return {
                    "status": "error",
                    "message": "The meeting could not be deleted",
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Exception occured in fetching meeting details : {e}",
            }

    # this function is used to get the recording data of the meeting
    def get_meeting_recording_url(self, meeting_key: str):
        try:
            url = f"https://meeting.zoho.in/meeting/api/v2/{self.__get_zsoid()}/recordings/{meeting_key}.json"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                json_response = response.json()
                play_url = json_response["recordings"][0]["playUrl"]
                return {
                    "status": "success",
                    "message": "The Meeting recording details were fetched",
                    "data": play_url,
                }  
            else:
                return {
                    "status": "error",
                    "message": "The meeting recording details could not be fetched",
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Exception occured in fetching meeting recording details : {e}",
            }

