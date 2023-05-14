import json
import os
import requests


# wechat
WX_APP_ID = os.environ['WX_APP_ID'] if os.environ.__contains__('WX_APP_ID') else 'wx74b2043f9f24c928'
WX_APP_SECRET = os.environ['WX_APP_SECRET'] if os.environ.__contains__('WX_APP_SECRET') else 'a7468306e935e67097f43270a4b0dc13'
WX_TEMPLATE_ID = os.environ['WX_TEMPLATE_ID'] if os.environ.__contains__('WX_TEMPLATE_ID') else '65PHtCLUJbLABGyjVirGQlGi9rHnOhIq3zE9z36-bZc'
# pushdeer
PUSH_DEER_KEY = os.environ['PUSH_DEER_KEY'] if os.environ.__contains__('PUSH_DEER_KEY') else 'PDU21978TagRhUtBTvxub8ziAncb4WJ0ycsIS1NnX'


def push_wechat_message(content: str, link='https://hhsd.work/static/messages.html'):
    # Get token
    response = requests.get("https://api.weixin.qq.com/cgi-bin/token", params={
        "grant_type": "client_credential",
        "appid": WX_APP_ID,
        "secret": WX_APP_SECRET
    })
    res = response.json()
    if "access_token" in res:
        token = res["access_token"]
        response = requests.get("https://api.weixin.qq.com/cgi-bin/user/get", {
            "access_token": token,
            "next_openid": ''
        })
        for open_id in response.json()['data']['openid']:
            body = {
                "touser": open_id,
                'template_id': WX_TEMPLATE_ID,
                'url': link,
                "topcolor": "#667F00",
                "data": {
                    "results": {
                        "value": content
                    }
                }
            }
            headers = {"Content-type": "application/json"}
            data = json.JSONEncoder().encode(body)
            print(data)
            requests.post(url=f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}",
                          data=data, headers=headers)
    else:
        print(f"Error:{response.json()}")


def push_pushdeer_message(content: str):
    response = requests.get("https://api2.pushdeer.com/message/push", params={
        "pushkey": PUSH_DEER_KEY,
        "text": content
    })
    print(response.text)
