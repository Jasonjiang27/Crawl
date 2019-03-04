import urllib, sys
import urllib.request
import urllib.error
import ssl

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=G1f2BvRMgxfq58fkTL4IDPYG&client_secret=99HgqW0cGtK6DPnIdYwI7cAF0iKtWuUI'
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
if (content):
    print(content)