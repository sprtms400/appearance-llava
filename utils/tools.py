import os
import base64

def image_path_to_base64(image_path):
    if not os.path.exists(image_path):
        raise Exception('Image not found')
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
        return encoded_string.decode('utf-8')
    
def image_to_base64(image):
    encoded_string = base64.b64encode(image)
    return encoded_string.decode('utf-8')