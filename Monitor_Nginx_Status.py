#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2023/4/8 17:05
# file: Monitor_Nginx_Status.py
# author: qinxi
# email: 1023495336@qq.com
import base64
import hashlib
import hmac
import json
import os
import socket
import time
import requests
import datetime


NOW_TIME = datetime.datetime.now()
HOST = socket.gethostname()
SECRET = ""
FEISHU_HOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/be******5e21"

def generate_signature(timestamp, secret):
    """
    生成飞书机器人消息签名
    """
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


def send_feishu_message(message):
    """
    发送text类型飞书消息通知
    """
    timestamp = int(time.time())
    title = "测试环境服务监控"
    sign = generate_signature(timestamp, SECRET)
    headers = {"Content-Type": "application/json;charset=utf-8"}
    message_body = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [[{"tag": "text", "text": message}]]
                }
            }
        }
    }
    try:
        res = requests.post(FEISHU_HOOK_URL, data=json.dumps(message_body), headers=headers)
        res = res.json()
    except Exception as e:
        print.error("请求异常: %s" % e)
        res = None

    return res

if __name__ == '__main__':
    # 检查 Nginx 进程是否存在
    cmd = "ps aux | grep nginx | grep -v grep"
    result = os.popen(cmd).readlines()
    if len(result) > 0:
        # Nginx 正在运行
        # time.sleep(10)
        print(str(NOW_TIME) +' '+ HOST+' 服务器 Nginx 正在运行')
    else:
        # Nginx 没有运行
        print(str(NOW_TIME) +' '+ HOST+" Nginx 没有运行，正在重启...")
        os.system("nginx")
        send_feishu_message(HOST+" 服务器 Nginx 正在重启......")
        
        
        
