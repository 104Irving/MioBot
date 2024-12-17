import json
from src.CommandDecoder import CommandDecoder

# 使用flask建立一个简单的监听后端
from flask import Flask, request

# import subprocess

app = Flask(__name__)
with open("./config/config.json", "rt", encoding="utf-8") as f:
    j_data = json.load(f)
post_bot = CommandDecoder(j_data["picture_file_path"])
group = j_data["monitor_group"]
# NapCatQQ API的基础URL
base_url = "http://127.0.0.1:3000"


@app.route('/', methods=['POST'])
def receive_event():
    # subprocess.run([".\\NapCat\\launcher.bat", '2032509947'], check=True)

    while True:
        data = request.json
        # print("Received event:", data)

        # 检查是否是群消息事件并且是目标群消息
        if data['post_type'] == 'message' and data['message_type'] == 'group' and data['group_id'] in group:
            # 提取消息内容并确保是字符串
            message_objects = data['message']
            message = ''.join([m['data']['text'] for m in message_objects if m['type'] == 'text'])
            print(f"[msg][Msg_scr-{data['message_type']}]: {message}")

            # if 'test' in message:
            #     send_group_message(group, "hello world")

            post_bot.command_decoder(data)

        return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
