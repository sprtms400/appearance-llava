import requests
import json
import os 
import re

LLAVA_CONFIG_PATH = 'config/llava_config.json'
ZEROSHOT_TEMPLATE_PATH = 'config/zeroshot_template.json'
# {
#     "llava" : {
#         "protocol": "http",
#         "host": "localhost",
#         "port": "40000"
#     }
# }

def read_config(filepath):
    if not os.path.exists(filepath):
        raise Exception(f'{filepath} not found')
    with open(filepath) as f:
        return json.load(f)

def mail_service(prompt, temperature, top_p, max_new_tokens, stop):
    config = read_config(LLAVA_CONFIG_PATH)
    url = f"{config['llava']['protocol']}://{config['llava']['host']}:{config['llava']['port']}"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Package not accepted by llava')

# def prompt_generator():
#     config = read_config(ZEROSHOT_TEMPLATE_PATH)
#     print('config:', config)
#     print('config[\'requirements_to_assistant\']:', config['requirements_to_assistant'])
#     basic_prompt = config['requirements_to_assistant']
#     format_requirements = config["analyze_answer_format"]
#     full_prompt = basic_prompt + ' ' + str(format_requirements) + ', From this, What is he wearing at the image? answer with format. ASSISTANT:",'
#     print('full_prompt:', full_prompt)
#     return full_prompt

def prompt_generator():
    basic_prompt = 'A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human\'s questions. USER: <image> You have to follow format of answer This is the format '
    format_requirements = {
        "sex": "The sex who in the image",
        "helmet": {
            "isWearing" : "True of Not",
            "color" : "The color of the helmet",
            "dedcription" : "Explain about helmet"
        },
        "eyewear": {
            "isWearing" : "True of Not",
            "color" : "The color of the eyewear",
            "dedcription" : "Explain about eyewear"
        },
        "upper": {
            "sleeve": "long_sleeve or short_sleeve",
            "color" : "The color of the upper",
            "dedcription" : "Explain about upper"
        },
        "lower": {
            "sleeve": "long_sleeve or short_sleeve",
            "color" : "The color of the lower",
            "dedcription" : "Explain about lower"
        },
        "socks": {
            "isWearing" : "True of Not",
            "color" : "The color of the socks",
            "dedcription" : "Explain about socks"
        },
        "shoes": {
            "isWearing" : "True of Not",
            "color" : "The color of the shoes",
            "dedcription" : "Explain about shoes"
        },
        "gloves": {
            "isWearing" : "True of Not",
            "color" : "The color of the gloves",
            "dedcription" : "Explain about gloves"
        },
        "bicycle": {
            "isRiding" : "True of Not",
            "color" : "The color of the bicycle",
            "dedcription" : "Explain about bicycle"
        }
    }
    last_prompt = ', From this, What is he wearing at the image? answer with format. ASSISTANT:,'
    last_prompt_jsoned = json.dumps(format_requirements)
    last_prompt_jsoned.replace('"', '\"')
    full_prompt = basic_prompt + ' ' + json.dumps(format_requirements) + ' ' + last_prompt
    return last_prompt_jsoned.replace('"', '\\"')

def package_service(prompt, temperature, top_p, max_new_tokens, stop, base64_image):
    config = read_config(LLAVA_CONFIG_PATH)
    url = f"{config['llava']['protocol']}://{config['llava']['host']}:{config['llava']['port']}/worker_generate_stream"
    
    body = {
        "prompt": 'A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human\'s questions. USER: <image> You have to follow format of answer This is the format  {\"sex\": \"The sex who in the image\", \"helmet\": {\"isWearing\": \"True of Not\", \"color\": \"The color of the helmet\", \"dedcription\": \"Explain about helmet\"}, \"eyewear\": {\"isWearing\": \"True of Not\", \"color\": \"The color of the eyewear\", \"dedcription\": \"Explain about eyewear\"}, \"upper\": {\"sleeve\": \"long_sleeve or short_sleeve\", \"color\": \"The color of the upper\", \"dedcription\": \"Explain about upper\"}, \"lower\": {\"sleeve\": \"long_sleeve or short_sleeve\", \"color\": \"The color of the lower\", \"dedcription\": \"Explain about lower\"}, \"socks\": {\"isWearing\": \"True of Not\", \"color\": \"The color of the socks\", \"dedcription\": \"Explain about socks\"}, \"shoes\": {\"isWearing\": \"True of Not\", \"color\": \"The color of the shoes\", \"dedcription\": \"Explain about shoes\"}, \"gloves\": {\"isWearing\": \"True of Not\", \"color\": \"The color of the gloves\", \"dedcription\": \"Explain about gloves\"}, \"bicycle\": {\"isRiding\": \"True of Not\", \"color\": \"The color of the bicycle\", \"dedcription\": \"Explain about bicycle\"}} , From this, What is he wearing at the image? answer with format. ASSISTANT:',
        "temperature": temperature,
        "top_p": top_p,
        "max_new_tokens": max_new_tokens,
        "stop": stop,
        "images": [base64_image]
    }
    response = requests.post(url, json=body)
    if response.status_code == 200:
        data = response.content # Binary 형태로 접근할것.
        messages = data.split(b'\x00')
        converted_messages = []
        important_message = messages[:-1]
            
        for i in range(len(messages)-1):
            parsed_msg = json.loads(messages[i].decode('utf-8'))
            converted_messages.append(parsed_msg)

        # "ASSISTANT:" 이후에 등장하는 문자열에 대해서만 검색.
        answer = converted_messages[-1]["text"] #converted_messages 는 dict 형태
        start_index = answer.find('ASSISTANT:')
        extracted_text = answer[start_index + len('ASSISTANT:'):]
        print('extracted_text:', extracted_text)
        parsed_text = json.loads(extracted_text)
        return parsed_text