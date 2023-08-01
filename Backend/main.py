from dotenv import load_dotenv  # allows for us to get .env values
import os  # operating system
import base64  # type of encoding library
import json
from requests import post  # allows us to send a post request

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
# print(client_id, client_secret)
# authorization and authentication works differently depending on the type of api I'm using
# since we're using a cli script, we're using a client credentials flow
# and not a users credentials workflow
# we will use base 64 encoding to retrieve and concat our token response


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    # notice: headers= header information, data= body of my request
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


token = get_token()
print(token)
# notice that different tokens are provided everytime we invoke this function
