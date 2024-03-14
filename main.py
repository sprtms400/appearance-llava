#%%
from utils import task_collector, asset_getter, tools, uploader
import restful_interface.prompt_combinator as prompt_combinator
import restful_interface.comunicator as comunicator
import time

if __name__ == "__main__":
    i = 0  
    while True:
        time.sleep(2)
        photoId_bytes = task_collector.get_messages_once()
        photoId = photoId_bytes.decode('utf-8')
        print(f'[{i}] photoId: {photoId}')
        i+=1
        
        # 시도시 실패한 목록, 추후 수동으로 업데이트 필요
        # photoId = '3d1761ef5edd4852b0d7f4ad1e0ca899'
        # photoId = 'b78006c10983419b96369c57da61cc35'
        # photoId = '6adc2f0a48214446ab5cd02bd0502687'
        # photoId = '3d1761ef5edd4852b0d7f4ad1e0ca899'
        # photoId = '9c0ec7fe917344e0b047a74b0599ba3d'
        
        if (photoId == 'b78006c10983419b96369c57da61cc35'):
            continue
        if (photoId == None):
            print('There is no more message in the queue.')
            break
            
        asset = asset_getter.get_asset(photoId)
        if asset is None:
            print('There is no asset for the photoId')
            break
        base64_image = tools.image_to_base64(asset)
        request_prompt = " "
        temperature = 0.2
        top_p = 0.7
        max_new_tokens = 512
        stop = '</s>'
        result_dict = comunicator.package_service(None, temperature, top_p, max_new_tokens, stop, base64_image)
        uploader.updateAppearance(photoId, result_dict)
        uploader.checkAppearanceAnalyzed(photoId)