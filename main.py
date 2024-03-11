#%%
from utils import task_collector, asset_getter, tools, uploader
import restful_interface.prompt_combinator as prompt_combinator
import restful_interface.comunicator as comunicator
import time

if __name__ == "__main__":
    print("Hello, World!")  
    while True:
        time.sleep(2)
        # photoId_bytes = task_collector.get_messages_once()
        # photoId = photoId_bytes.decode('utf-8')
        photoId = 'b78006c10983419b96369c57da61cc35'
        if (photoId == None):
            print('There is no more message in the queue.')
            break
        
        asset = asset_getter.get_asset(photoId)
        if asset is None:
            break
        base64_image = tools.image_to_base64(asset)
        request_prompt = " "
        temperature = 0.2
        top_p = 0.7
        max_new_tokens = 512
        stop = '</s>'
        result_dict = comunicator.package_service(None, temperature, top_p, max_new_tokens, stop, base64_image)
        uploader.updateAppearance(photoId, result_dict)
        # uploader.checkAppearanceAnalyzed(photoId)
        break