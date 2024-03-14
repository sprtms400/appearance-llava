#%%
import json
import requests
import pika

def read_config():
    with open('../config/apiserver_connection.json', 'r') as f:
        return json.load(f)
    
    
api_config = read_config()
protocol = api_config["gfps"]["protocol"]
server_url = api_config["gfps"]["host"]
port = api_config["gfps"]["port"]
full_url = f'{protocol}://{server_url}:{port}/photos'

photos = requests.get(full_url)

photo_list = []
analyzed_photo_list = []
unAnalyzed_photo_list = []

for photo in photos.json():
    print(photo['photoId'])
    photo_list.append(photo['photoId'])
    if photo['isPhotoAnalyzedAppearance'] is True:
        analyzed_photo_list.append(photo['photoId'])
    if photo['isPhotoAnalyzedAppearance'] is False:
        unAnalyzed_photo_list.append(photo['photoId'])
        
print('len(photo_list):', len(photo_list))
print('len(analyzed_photo_list):', len(analyzed_photo_list))
print('len(unAnalyzed_photo_list):', len(unAnalyzed_photo_list))

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='analyzingQueueAppearance', durable=True)

for photo in unAnalyzed_photo_list:
    data = photo.encode()
    channel.basic_publish(exchange='', routing_key='analyzingQueueAppearance', body=data)
    print(f"Sent {photo} to the queue.")  