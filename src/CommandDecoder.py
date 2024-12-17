import os
import re
from random import choice, randint

from src.BotSerever import *


# 对任意第一个列表中的字符串str1，总能在第二个列表中找到一个字符串str2，使得str1是str2的连续子串。
def is_substr(main_lst, substr_lst):
    # 遍历第一个列表中的每个字符串
    for main_str in main_lst:
        # 假设当前字符串不是任何字符串的子串
        is_substr_ = False
        # 遍历第二个列表中的每个字符串
        for substr in substr_lst:
            # 如果当前字符串是子串，则设置标志为True并跳出循环
            if main_str in substr:
                is_substr_ = True
                break
        # 如果当前字符串不是任何字符串的子串，则返回False
        if not is_substr_:
            return False
    # 如果所有字符串都是子串，则返回True
    return True


def bool_seek_by_tag(key_word_group, data):
    return is_substr(key_word_group, data["origin_tag"]) or is_substr(key_word_group, data["origin_tag"])


def bool_seek_by_uid(key_word_group, data):
    return data['UID'] in key_word_group


# 解析指令并调用对应发送消息api的类
class CommandDecoder(object):
    def __init__(self, picture_file_path):
        self.bot = PostMessage()
        self.config_path = "./config"
        self.picture_file_path = picture_file_path
        self.picture_path = f"{self.picture_file_path}Artwork\\"

        self.user_dict = {}
        with open(f"{self.picture_file_path}Uid_List.txt", 'rt', encoding="utf-8") as f:
            while True:
                line = f.readline()
                if line == "": break
                line = line.split(":")
                self.user_dict[line[0]] = line[1]

    def __del__(self):
        pass

    def search_pic(self, keyword_group, mode_func):
        pid_list = os.listdir(self.picture_path)
        if not keyword_group:
            return pid_list

        out_come = []
        for pid in pid_list:
            with open(f"{self.picture_path}{pid}\\tags.json", "rt", encoding="utf-8") as f:
                data = dict(json.load(f))
                if 'r18_mode' not in data or data['r18_mode'] == 'r18':
                    continue

                if mode_func(keyword_group, data):
                    out_come.append(pid)
        return out_come

    def search_uid_by_name(self, key_word_group):
        uid_list = []
        for key_word in key_word_group:
            if key_word.isdigit():
                uid_list.append(key_word)
                continue
            for uid in self.user_dict.keys():
                if key_word in self.user_dict[uid]:
                    uid_list.append(uid)
        return uid_list

    # 接收指令源格式并解析翻译调用各个指令的函数
    def command_decoder(self, data):
        msg = data["message"][0]

        # 非文本类型消息暂不解析
        if msg['type'] != 'text':
            return

        # 骰子类指令
        if msg["data"]["text"][0] == ".":
            return self.roll_dice(data)

        # 点图类指令
        if ("picture" or "p") in msg["data"]["text"]:
            return self.post_picture(data)

    def cmd_help(self):
        pass

    def post_picture(self, data):
        payload = get_payload()
        payload = msg_append_group_id(payload, data['group_id'])

        command = data["message"][0]["data"]['text']
        pattern = r'^picture\s+-(\w+)\s*(?:([^\s]+(?:\s+[^\s]+)*))?$'

        # 使用正则表达式解析命令
        match = re.match(pattern, command)

        if match:
            # 将匹配的模式赋值给变量
            mode = match.group(1)

            # 如果存在关键字组，则分割成单词列表，否则为一个空列表
            keyword_group = match.group(2)
            keyword_group = keyword_group.strip().split() if keyword_group else []

        else:
            payload = msg_append_text(payload, 'Invalid dice command!')
            return self.bot.send_group_msg(payload)

        # 检索
        # 按照tag检索
        out_come = []
        if "t" in mode:
            out_come = self.search_pic(keyword_group, bool_seek_by_tag)
        # 按照pid检索
        elif "p" in mode:
            for pid in keyword_group:
                out_come.append(pid if os.path.isdir(f'{self.picture_path}{pid}') else None)
        # 按照uid检索
        elif "u" in mode:
            uid_list = self.search_uid_by_name(keyword_group)
            if not uid_list:
                payload = msg_append_text(payload, f"检索到{len(out_come)}个作者")
                return self.bot.send_group_msg(payload)

            out_come = self.search_pic(uid_list, bool_seek_by_uid)

        # 检索结果为0
        if not out_come:
            # payload = msg_append_text(payload, f"检索到{len(out_come)}个结果")
            payload = msg_append_text(payload, f"罢工了喵")
            return self.bot.send_group_msg(payload)

        if "r" in mode:
            pid = choice(out_come)

            with open(f"{self.picture_path}{pid}\\tags.json") as f:
                data = json.load(f)

            pic_list = (os.listdir(f"{self.picture_path}{pid}"))
            pic_list.remove("tags.json")

            payload = msg_append_text(payload, f"检索到{len(out_come)}个结果, 选择pid:{pid}作为结果\n")
            # payload = msg_append_text(payload, f"作者:{self.user_dict[data["UID"]]}uid:{data["UID"]}\n")
            payload = msg_append_text(payload, f"更新时间:{data["uploaded_date"].split('T')[0]}\n")
            for p in pic_list:
                payload = msg_append_pic(payload, f"{self.picture_path}{pid}\\{p}")
            return self.bot.send_group_msg(payload)

    # 投骰子的指令
    def roll_dice(self, data):
        payload = get_payload()
        payload = msg_append_group_id(payload, data['group_id'])

        message = data["message"][0]["data"]['text']
        pattern = r'\.r(\d*)d(\d+)(?:\+(\d+))?'
        match = re.match(pattern, message)
        if not match:
            payload = msg_append_text(payload, 'Invalid dice command!')
            return self.bot.send_group_msg(payload)

        # 提取骰子数量、面数和额外加数
        num_dice = int(match.group(1)) if match.group(1) else 1  # 如果没有指定骰子数量，默认为1
        sides_per_dice = int(match.group(2)) if match.group(2) else 100  # 如果没有指定骰子面数 默认为100
        additional = int(match.group(3)) if match.group(3) else 0  # 如果没有指定额外加数，默认为0

        # 生成随机数并计算总和
        rolls = [randint(1, sides_per_dice) for _ in range(num_dice)]
        result = sum(rolls) + additional

        # 格式化输出
        rolls_str = '+'.join(map(str, rolls))
        out_str = f'{str(data['sender']['nickname'])}投掷{message}={rolls_str}={result}'

        payload = msg_append_text(payload, out_str)
        return self.bot.send_group_msg(payload)


def main():
    with open(f"E:\\Picture\\Artwork\\{1127456}\\tags.json") as f:
        data = dict(json.load(f))
    uid = ["217707"]
    # test = CommandDecoder()
    print(data["UID"] in uid)
    pass


if __name__ == '__main__':
    main()
