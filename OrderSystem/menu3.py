import requests

headers = {"Authorization":"Bearer DXeo55kLJZhZWtaq80wFE0n2J2PI54xr39W9BriWscC1iyWDoeTRLjTTsOQaIONKnXgkprjYe3QxgEljRqbnl4K/P4duxVAyvnhiv+Eh0q1mcHmMwzDq2MDvTXGdvTKSFn0xO+yDD9LoHHYP8OQABwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-0cd3fc93d50b9d6588adbcf9c7d2b230', 
                       headers=headers)

print(req.text)
