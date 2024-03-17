#%% 

import json
import requests
import time

def read_config():
    with open('../config/apiserver_connection.json', 'r') as f:
        return json.load(f)

def reqeustAssetInfos(protocol, server_url, port, endpoint):
    full_url = f'{protocol}://{server_url}:{port}/{endpoint}'
    response = requests.get(full_url)
    print('full_url:', full_url)
    print('response:', response)
    response_parse = response.json()
    print('len(response_parse):', len(response_parse))
    print('type(response_parse : ', type(response_parse))
    print('response_parse[0]:', response_parse[0])
    return response_parse

def uploadDescrtiption(photoId, photoAppearDecription):
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    full_url = f'{protocol}://{server_url}:{port}/photo/{photoId}/uploadDescription'
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "appearDescription": photoAppearDecription
    }
    response = requests.post(full_url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to upload appearance. {response.status_code}")
        print(response.content)
    return response

def uploadDescriptions(bulk):
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    full_url = f'{protocol}://{server_url}:{port}/photo/uploadDescriptions'
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "appearDescriptions": bulk
    }
    response = requests.post(full_url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to upload appearance. {response.status_code}")
        print(response.content)
    return response

def get_asset_infos():
    api_config = read_config()
    asset_info = reqeustAssetInfos(api_config["gfps"]["protocol"], api_config["gfps"]["host"], api_config["gfps"]["port"], 'photos')
    return asset_info

def extract_appearance_info(photoDict):
    if photoDict["isPhotoAnalyzedAppearance"]:
        return photoDict["appearance"]
    else:
        return None

def is_appear_disc_already_analyzed(appearance_dict):
    if appearance_dict["description"] is 'unknown':
        return True
    else:
        return False

def make_description(appearance_dict):
    sex_description = ''
    helmet_color_description = ''
    eyewear_color_description = ''
    upper_sleeve_description = ''
    upper_color_description = ''
    upper_total_description = ''
    lower_sleeve_description = ''
    lower_color_description = ''
    lower_total_description = ''
    # socks_color_description = ''
    shoes_color_description = ''
    gloves_color_description = ''
    bicycle_color_description = ''
    
    if appearance_dict["sex"]:
        sex_description = f'A {appearance_dict["sex"]}'
    if appearance_dict["helmet"]["isWearing"] and appearance_dict["helmet"]["color"]:
        helmet_color_description = f' is wearing a {appearance_dict["helmet"]["color"]} helmet.'
    if appearance_dict["eyewear"]["isWearing"] and appearance_dict["eyewear"]["color"]:
        eyewear_color_description =  f'{appearance_dict["eyewear"]["color"]} eyewear,'
    if appearance_dict["upper"]["sleeve"] and appearance_dict["upper"]["color"]:
        upper_sleeve_description = appearance_dict["upper"]["sleeve"]
        upper_color_description = appearance_dict["upper"]["color"]
        upper_total_description = f'{upper_sleeve_description} {upper_color_description} upper,'
    if appearance_dict["lower"]["sleeve"] and appearance_dict["lower"]["color"]:
        lower_sleeve_description = appearance_dict["lower"]["sleeve"]
        lower_color_description = appearance_dict["lower"]["color"]
        lower_total_description = f'{lower_sleeve_description} {lower_color_description} lower,'
    # if appearance_dict["socks"]["isWearing"] and appearance_dict["socks"]["color"]:
    #     pass
    if appearance_dict["shoes"]["isWearing"] and appearance_dict["shoes"]["color"]:
        shoes_color_description = f'{appearance_dict["shoes"]["color"]} shoes,'
    if appearance_dict["gloves"]["isWearing"] and appearance_dict["gloves"]["color"]:
        gloves_color_description = f'{appearance_dict["gloves"]["color"]} gloves'
    if appearance_dict["bicycle"]["color"]:
        bicycle_color_description = f'and riding a {appearance_dict["bicycle"]["color"]} bicycle,'
        
    total_description = sex_description + helmet_color_description + eyewear_color_description + upper_total_description + lower_total_description + shoes_color_description + gloves_color_description + bicycle_color_description + '.'
    return total_description

appearances = get_asset_infos()
i = 0
for appearance in appearances:
    i += 1
    if i < 510:
        continue
    appearance_info = extract_appearance_info(appearance)
    if is_appear_disc_already_analyzed(appearance_info) == False:
        time.sleep(2)
        full_description = make_description(appearance_info)
        print('full_description:', full_description)
        response = uploadDescrtiption(appearance["photoId"], full_description)
        parsed_response = response.json()
        print(parsed_response)
    else:
        print('already analyzed.')
print('len(appearances):', len(appearances))

# bulk = []
# appearances = get_asset_infos()
# for appearance in appearances:
#     appearance_info = extract_appearance_info(appearance)
#     appearDescription = make_description(appearance_info)
#     photoId = appearance["photoId"]
#     box = {
#         "photoId": photoId,
#         "appearDescription": appearDescription
#     }
#     bulk.append(box)

# print('len(bulk):', len(bulk))
# response = uploadDescriptions(bulk)
# parsed_response = response.json()
# print('len(parsed_response):', len(parsed_response))