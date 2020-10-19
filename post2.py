#coding=utf-8
import requests
import time
import base64

t1 = time.time()
s = requests
with open('6.jpg', 'rb') as f:
    imgbase64 = base64.b64encode(f.read())
data={'keyword':'中国人'}
r = s.post('http://0.0.0.0:8082/upkeywords', data)

print(r.text)
print('time cost:', time.time() - t1)
