import requests
json_url='https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
req=requests.get(json_url)

with open('btc_close_urllib.json','w') as f:
    f.write(req.text)
file_requests=req.json()