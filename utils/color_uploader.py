#%%
import json
import requests
import time

def read_config():
    with open('../config/apiserver_connection.json', 'r') as f:
        return json.load(f)
    
def uploadColor(color):
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    full_url = f'{protocol}://{server_url}:{port}/color/create'
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "color": color
    }
    response = requests.post(full_url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to upload appearance. {response.status_code}")
        print(response.content)
    return response

def get_distinct_colors_by_field(field):
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    full_url = f'{protocol}://{server_url}:{port}/photo/aggregate/color_by_field?field={field}'
    
    response = requests.get(full_url)
    if response.status_code != 200:
        print(f"Failed to upload appearance. {response.status_code}")
        print(response.content)
    return response

distinct_colors = []
fields = ['helmet', 'eyewear', 'upper', 'lower', 'socks', 'shoes', 'gloves', 'bicycle']
for field in fields:
    response = get_distinct_colors_by_field(field)
    colors = response.json()
    print(f'Field: {field}')
    print('colors:', colors)
    for color in colors:
        color = color.lower()
        if color.find(' and ') != -1: # and 가 있으면
            splited_colors = color.split(' and ')
            for splited_color in splited_colors:
                if splited_color not in distinct_colors:
                    distinct_colors.append(splited_color)
            continue
        if color not in distinct_colors:
            distinct_colors.append(color)

print('distinct_colors:', distinct_colors)
print('len(distinct_colors):', len(distinct_colors))
#%%
for field in fields:
    response = get_distinct_colors_by_field(field)
    colors = response.json()
    print(f'Field: {field}')
    print('colors:', colors)
    for color in colors:
        # 만약 color 가 Black and white 이면 Black, white 형태로 추출하는 코드
        if color.find(' and ') != -1: # and 가 있으면
            splited_colors = color.split(' and ')
            for splited_color in splited_colors:
                response = uploadColor(splited_color)
                if response.status_code != 200:
                    print(f"Failed to upload appearance. {response.status_code}")
                print(response.content)
            continue
        response = uploadColor(color)
        if response.status_code != 200:
            print(f"Failed to upload appearance. {response.status_code}")
        print(response.content)
        
