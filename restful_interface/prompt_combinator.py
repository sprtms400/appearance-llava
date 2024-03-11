import utils.tools as tools

import json
import os

def read_template():
    if not os.path.exists('config/zeroshot_template.json'):
        raise Exception('zeroshot_template.json not found')
    with open('config/zeroshot_template.json') as f:
        return json.load(f)
    
def text_prompt(prompt):
    templates_list = read_template()
    head_prompt = templates_list["assistant_requirements_for_text"]
    total_prompt = head_prompt + prompt
    return total_prompt
    
def image_prompt(prompt):
    templates_list = read_template()
    head_prompt = templates_list["assistant_requirements_for_image"]
    total_prompt = head_prompt + prompt
    return total_prompt
    
def combine_prompt(service, prompt):
    if service == "text":
        combined_prompt = text_prompt(prompt)
        combined_prompt = combined_prompt + 'ASSISTANT: '
    elif service == "image":
        combined_prompt = image_prompt(prompt)
        combined_prompt = combined_prompt + 'ASSISTANT: '
    else:
        raise Exception('Service not supported')
    return combined_prompt