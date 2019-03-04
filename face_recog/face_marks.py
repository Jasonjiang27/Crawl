import base64
import json
import requests

token = '24.7eaa65f998a4a9b8b5c969246cbfa1b9.2592000.1554303543.282335-15680992'

def get_img_base(file):
    
    with open(file,'rb') as fp:
        content = base64.b64encode(fp.read())
        return content

request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
request_url = request_url + "?access_token=" + token

params = {
    
'image':get_img_base('test1.jpg'),
    
'image_type':'BASE64',
    
'face_field':'age,beauty,gender'
}

res = requests.post(request_url,data=params)
result = res.text
json_result = json.loads(result)
code = json_result['error_code']
gender = json_result['result']['face_list'][0]['gender']['type']
beauty = json_result['result']['face_list'][0]['beauty']
print(code,gender,beauty)
