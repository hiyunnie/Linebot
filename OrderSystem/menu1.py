import requests
import json

headers = {"Authorization":"Bearer <Channel access token>","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Menu",
    "chatBarText": "點我收合選單",
    "areas":[
        # {
        #   "bounds": {"x": 551, "y": 325, "width": 321, "height": 321},
        #   "action": {"type": "message", "text": "up"}
        # },
        # {
        #   "bounds": {"x": 876, "y": 651, "width": 321, "height": 321},
        #   "action": {"type": "message", "text": "right"}
        # },
        # {
        #   "bounds": {"x": 551, "y": 972, "width": 321, "height": 321},
        #   "action": {"type": "message", "text": "down"}
        # },
        {
          "bounds": {"x": 0, "y": 843, "width": 830, "height": 830},
          "action": {"type": "message", "text": "我要下單"}
        },
        {
          "bounds": {"x": 833, "y": 843, "width": 830, "height": 830},
          "action": {"type": "message", "text": "訂單查詢"}
        },
        {
          "bounds": {"x": 1666, "y": 843, "width": 830, "height": 830},
          "action": {"type": "message", "text": "營業資訊"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)

