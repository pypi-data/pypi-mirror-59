#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time : 2019/2/14 0014
# @Email : jtyoui@qq.com
import requests
from jtyoui.web import random
from jtyoui.error import LibraryNotInstallError
import re

try:
    import itchat  # 安装 pip install itchat
except ModuleNotFoundError:
    raise LibraryNotInstallError("安装 pip install itchat")

url = 'https://m.xunleige.com/'


def movie(name):
    param = dict(searchword=name.encode('gb2312'))
    response = requests.post(url + 'search.asp', data=param, headers={'User-Agent': random()})
    response.encoding = 'GBK'
    data = response.text
    find, = re.findall(pattern=r'<div class="list mb">(.+)</div>', string=data, flags=re.S)
    message = re.findall(pattern='a href="(.+)" title="(.+)" class', string=find)
    return message


@itchat.msg_register(itchat.content.TEXT)  # 获得文本信息
def text_reply(msg):
    message = msg.text
    if message.startswith('@'):
        text = movie(message[1:])
        for u, t in text:
            itchat.send_msg(t + ': ' + url + u, msg['FromUserName'])


def movie_start():
    itchat.auto_login(hotReload=True)
    itchat.run()


if __name__ == '__main__':
    movie_start()
