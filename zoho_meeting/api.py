import requests
import json
import datetime
from typing import Union
import pytz

# the presented ID will be sent as an argument when an object is created and a function is called, as it should not be related to the class but that specific call to the object
# the access token for each user(presenter) should be different? - if so renew_access_token cannot be a class method


class ZohoMeetingAPI:

    # class variables

    def __init__(self, client_id, client_secret, access_token, refresh_token):
        self.client_id = client_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.zsoid = None
        self.zuid = None
        self.renew_access_token(refresh_token, client_id, client_secret)

    @staticmethod
    def create_access_token():  # do we have to create an access token from scratch here? or just make the user pass it?
        # get the authroization grant
        # send it to receive an access and refresh token
        # send the request to renew access token
        pass

    @staticmethod
    def create_refresh_token():
        pass

    @staticmethod
    def has_meeting_ended(meetingKey: str, endTime: str, currentTime: datetime):
        # Convert the provided end time to a datetime object
        provided_date_time = datetime.strptime(endTime, "%b %d, %Y %I:%M %p")
        provided_date_time_aware = provided_date_time.replace(
            tzinfo=pytz.timezone("Asia/Kolkata")
        )
        # Compare the two datetime objects
        if currentTime <= provided_date_time_aware:
            print("The meeting has not ended")
            return False
        else:
            print("The meeting has ended")
            return True

    # this function is used to get the ZSOID keys, to be by the user to interact
    def get_user_info(self):
        try:
            get_user_info_url = "https://meeting.zoho.in/api/v2/user.json"
            headers = {
                "Authorization": f"Zoho-oauthtoken {self.access_token}",
                "Content-Type": "application/json",
            }
            response = requests.get(get_user_info_url, headers=headers)
            parsed_response = response.json()
            return {
                "status": "success",
                "message": f"User details are: {parsed_response}",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Exception occured in getting user details",
            }

    # this function is used to renew the access token using the refresh token
    def renew_access_token(
        self, refresh_token: str, client_id: str, client_secret: str
    ):

        # check if current access token has expired
        check_token_expiration_url = "https://meeting.zoho.in/api/v2/user.json"
        headers_for_verification = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/json",
        }
        verification_response = requests.request(
            "GET", check_token_expiration_url, headers=headers_for_verification
        )

        if verification_response.status_code != 200:
            # if has expired, regenerate with refresh token
            renew_access_token_url = f"https://accounts.zoho.in/oauth/v2/token?refresh_token={self.refresh_token}&client_id={self.client_id}&client_secret={self.client_secret}&redirect_uri=http://43.204.149.165:8000/&grant_type=refresh_token"
            headers = {"Content-Type": "application/json"}

            new_access_token_response = requests.post(
                renew_access_token_url, headers=headers
            )

            if new_access_token_response.status_code == 200:
                response_data = new_access_token_response.json()
                self.access_token = response_data.get("access_token")
                user_info_response = self.get_user_info()
                user_name = user_info_response["userDetails"]["fullName"]
            else:
                print("Can't renew access token")

        # else continue to use the same access token
        else:
            print("The access token is not expired yet")

    # this function is used to create the meeting
    def scheduleMeeting(
        self,
        topic: str,
        startTime: str,
        timezone: str,
        presenterId: int,
        duration: Union[int, None] = None,
        participants: list = None,
    ):
        request_url = f"https://meeting.zoho.in/api/v2/{self.zsoid}/sessions.json"
        presenterId = self.zuid
        print(presenterId)
        payload = json.dumps(
            {
                "session": {
                    "topic": topic,
                    "startTime": startTime,
                    "presenter": presenterId,
                    "timezone": timezone,
                    "participants": participants,
                    # "participants": [
                    # # []
                    # {
                    #     # "email": "mangesh.singh@codenia.in",
                    #     "email": "radhika.kakkar@corewebconnections.com",
                    # }
                    # ]
                }
            }
        )

        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/json;charset=UTF-8",
        }
        try:
            response = requests.post(request_url, headers=headers, data=payload)
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
            f"https://meeting.zoho.in/api/v2/{self.zsoid}/sessions/{meetingKey}.json"
        )
        presenterId = self.zuid
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/json;charset=UTF-8",
        }
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
                "PUT", request_url, headers=headers, data=payload_json
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
            f"https://meeting.zoho.in/api/v2/{self.zsoid}/sessions/{meetingKey}.json"
        )
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/json;charset=UTF-8",
        }
        try:
            response = requests.get(request_url, headers=headers)
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
            f"https://meeting.zoho.in/api/v2/{self.zsoid}/sessions/{meetingKey}.json"
        )
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/json;charset=UTF-8",
        }
        try:
            response = requests.delete(request_url, headers=headers)
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
            url = f"https://meeting.zoho.in/meeting/api/v2/{self.zsoid}/recordings/{meeting_key}.json"
            headers = {
                "Authorization": f"Zoho-oauthtoken {self.access_token}",
                "Content-Type": "application/json",
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_response = response.json()
                play_url = json_response["recordings"][0]["playUrl"]
                return {
                    "status": "success",
                    "message": "The Meeting recording details were fetched",
                    "data": play_url,
                }  # to sednd more data
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
