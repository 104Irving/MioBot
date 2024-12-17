以下是一些json格式文件的实例
```python
# receive消息示例
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

# 发送族群消息示例
group_post_msg_exp = {
    "group_id": "123456",
    "message": [{
        "type": "text",
        "data": {
            "text": "message"
        }
    },{
        "type": "image",
        "data": {
            "file": "filepath"
        }
    }]
}
```