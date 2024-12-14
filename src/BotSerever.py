import json

# 使用flask建立一个简单的监听后端
from flask import Flask, request

# 使用request库
import requests

app = Flask(__name__)
# NapCatQQ API的基础URL
base_url = "http://127.0.0.1:3000"


# 负责调用NapCat的API发送QQ消息的类
def response_callback(response):
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")
        print(response.status_code, response.text)


def msg_append_group_id(payload, group_id):
    payload["group_id"] = group_id
    return payload


def msg_append_pic(payload, file_path):
    payload["message"].append({
        "type": "image",
        "data": {
            "file": file_path
        }
    })
    return payload


def msg_append_text(payload, message):
    payload["message"].append({
        "type": "text",
        "data": {
            "text": message
        }
    })
    return payload


class PostMessage(object):
    def __init__(self):
        self.token = "a196wal9k0h"
        self.headers = {
            'Content-Type': 'application/json',
            "Authorization": self.token
        }

        self.payload = {
            "message": [],
        }

    def send_group_msg(self, params):
        url = f"{base_url}/send_group_msg"

        payload = json.dumps(params)
        response_callback(requests.request("POST", url, headers=self.headers, data=payload))
