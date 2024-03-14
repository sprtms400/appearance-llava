## 마라톤, 자전거 대회 사진에서의 인상착의 검출기
마라톤, 자전거 대회 사진에서 인상착의 정보를 추출합니다.
Vision LLM 인 LLava를 이용, 
정재된 출력형태를 In-Context Learing하여 인상착의에 대해 추출합니다.
추출하는 목록은 다음과 같습니다.

1. 성별
2. 헬멧 착용 여부와 색상
3. 고글혹은 선글라스의 착용 여부와 색상
4. 상의 긴팔/반판 여부와 색상
5. 하의 신바지/반바지 여부와 색상
6. 양말 착용 여부와 색상
7. 신발 색상
8. 자전거 탑승 여부와 색상

## 개발된 환경 및 구성

OS : Ubuntu 20.04

Python version : 3.10

Llava model : https://huggingface.co/liuhaotian/llava-v1.5-7b

구동하기 이전에 LLava 서비스를 구동시켜야합니다 
저장소 참조 : https://github.com/haotian-liu/LLaVA


### 마라톤, 그란폰도 대회 이미지 검색 서비스에서의 담당부분
![image](https://github.com/sprtms400/appearance-llava/assets/26298389/1151f74e-3c5d-411c-94de-1971e19c5000)


본 리포지터리에서는 마라톤, 그란폰도 대회 이미지 검색 서비스에서 녹색 박스에 해당된 부분을 담당합니다. 프로젝트에 대한 자세한 설명은
다음 저장소를 확인하세요.
https://github.com/sprtms400/Granfondo_Photo_Search/tree/main
