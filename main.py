import json
from src.CommandDecoder import CommandDecoder

# 使用flask建立一个简单的监听后端
from flask import Flask, request

# 使用request库
import requests

app = Flask(__name__)
# NapCatQQ API的基础URL
base_url = "http://127.0.0.1:3000"


@app.route('/', methods=['POST'])
def receive_event():
    post_bot = CommandDecoder()
    group = [860801719, 832981296]
    while True:
        data = request.json
        # print("Received event:", data)

        # 检查是否是群消息事件并且是目标群消息
        if data['post_type'] == 'message' and data['message_type'] == 'group' and data['group_id'] in group:
            # 提取消息内容并确保是字符串
            message_objects = data['message']
            message = ''.join([m['data']['text'] for m in message_objects if m['type'] == 'text'])

            # if 'test' in message:
            #     send_group_message(group, "hello world")

            post_bot.command_decoder(data, group)

        return "OK", 200


receive_exp = {
    'self_id': 2032509947,
    'user_id': 2939633973,
    'time': 1733986337,
    'message_id': 1518839298,
    'message_seq': 1518839298,
    'real_id': 1518839298,
    'message_type': 'group',
    'sender': {
        'user_id': 2939633973,
        'nickname': '式北',
        'card': '',
        'role': 'member'
    },
    'raw_message': '.rd100',
    'font': 14,
    'sub_type': 'normal',
    'message': [
        {
            'type': 'text',
            'data': {
                'text': '.rd100'
            }
        }
    ],
    'message_format': 'array',
    'post_type': 'message',
    'group_id': 860801719
}


if __name__ == '__main__':
    # send_group_picture(860801719)
    app.run(host='0.0.0.0', port=7777)
