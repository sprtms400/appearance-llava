import json
import requests
import utils.parser as parser

def read_config():
    with open('config/apiserver_connection.json', 'r') as f:
        return json.load(f)


def updateAppearance(photoId, appearance_dict): 
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    full_url = f'{protocol}://{server_url}:{port}/photo/{photoId}/appearance'
    
    headers = {'Content-Type': 'application/json'}
    parser.convert_string_to_bool(appearance_dict)
    data = {
        "appearance": appearance_dict
    }

    response = requests.post(full_url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to update appearance. {response.status_code}")
        print(response.content)
    return response
    
    
def checkAppearanceAnalyzed(photoId):
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    
    full_url = f'{protocol}://{server_url}:{port}/photo/{photoId}/checkAppearanceAnalyzed'
    response = requests.patch(full_url)
    if response.status_code != 200:
        print(f"Failed to check analyzed. {response.status_code}")
    return response