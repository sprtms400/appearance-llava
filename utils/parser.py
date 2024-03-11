import json
import re

def reverse_string(string):
    return string[::-1]

def extract_last_block(string):
    parsed_string = reverse_string(string)
    
    ## calculate distance between '{' and '}'
    distance = 0
    count = 0
    for w in parsed_string:
        if w == '}':
            count += 1
        if w == '{':
            count -= 1
            if count == 0:
                break
        distance += 1
        
    parsed_string = parsed_string[:distance+1]
    complete_string = reverse_string(parsed_string)
    return complete_string

# LLava 응답 인덱스 추출 및 반환
def extract_impinfo (block_string):
    pattern = r'{[^}]*}'
    matches = re.findall(pattern, block_string)
    # for word in block_string.split():
    #     if 'ASSISTANT:' in word:
    return matches[1]

def llava_parser(response_body):
    formatted_response= response_body.replace('\\', '')
    parsed_string = extract_last_block(formatted_response)
    extracted_string = extract_impinfo(parsed_string)
    extracted_string= extracted_string.encode('utf-8')
    decoded_string = extracted_string.decode('utf-8')
    
    print('decoded_string:', decoded_string)
    
    # 디코딩된 문자열을 직접 JSON으로 파싱
    jsoned = json.loads(decoded_string)
    
    return jsoned

def convert_string_to_bool(obj):
    for key, value in obj.items():
        if isinstance(value, dict):
            convert_string_to_bool(value)
        else:
            if value == 'True':
                obj[key] = True
            elif value == 'False':
                obj[key] = False