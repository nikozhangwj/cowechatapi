# !/usr/bin/env python
# encoding: utf-8
# author: niko.zhang
# py_ver: py3

"""
调用企业微信消息接口发送消息
可以指定某个用户、某个部门或者某个标签内的所有人员
初始化后需要调用login功能输入企业ID和消息应用密钥
密钥需要现在企业微信后台建立应用后才能获取
该功能需要在python3下的环境执行，不然会抱消息类型错误
"""
from urllib import request
from datetime import datetime
import json
import os


class Alert(object):

    def __init__(self):
        # 设置企业微信的coropid和corpsecret, cache用来缓存token
        self.ID = ''
        self.SECRET = ''
        self.cache = './.token_cache'

    # 不写死的话每次要先执行login
    def login(self, ID, SECRET):
        if not ID and not SECRET:
            print('Please input valid ID and SECRET.')
            return False
        self.ID = ID
        self.SECRET = SECRET
        return True

    # 用来保存token到缓存文件
    def save_token(self, token_dict):
        token_dict['date'] = datetime.strftime(datetime.now(), "%Y-%m-%d %H%M%S")
        with open(self.cache, 'wt') as fhandler:
            fhandler.write(json.dumps(token_dict, indent=4))

    # 通过时间判断token是否有效，token有效时间为两个小时
    def token_valid(self):
        if not os.path.exists(self.cache):
            return False
        with open(self.cache, 'rt') as fhandler:
            data = json.loads(fhandler.read())
            if data['errmsg'] != 'ok':
                print('Cache has no token but error message: '+data['errmsg'])
                return False
            else:
                print('Cache has no error message.')
                pass
            token_date = data['date']
            usetime=(datetime.now() - datetime.strptime(token_date, "%Y-%m-%d %H%M%S")).seconds
            if usetime >= 7200:
                print('Cache token is overtime, get new token from url.')
                return False
            else:
                print('Cache token is valid, get token from cache.')
                return True

    # 通过企业微信API重新获取token
    def get_access_token_url(self):
        token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(self.ID, self.SECRET)
        try:
            res = request.urlopen(token_url)
            # print(res.read())
        except BaseException as error:
            print(error)
            return False
        res_data = res.read()
        res_dict = json.loads(res_data.decode('utf-8'))
        print('Get token from url.')
        print(res_dict)
        try:
            res_dict.get('access_token')
        except KeyError as error:
            print(error)
            return False
        self.save_token(res_dict)
        return res_dict['access_token']

    # 通过缓存文件获取token
    def get_access_token_cache(self):
        with open(self.cache, 'rt') as fhandler:
            data = json.loads(fhandler.read())
            print('Cache token:')
            print(data)
            try:
                return data['access_token']
            except KeyError as error:
                print(error)
                return False

    # 获取token功能
    def get_access_token(self):
        if self.token_valid():
            return self.get_access_token_cache()
        else:
            return self.get_access_token_url()

    # 发送文本消息功能，支持发送用户、部门已经标签。
    # API使用可查看https://work.weixin.qq.com/api/doc#90000/90003/90487/%E6%B7%BB%E5%8A%A0%E8%87%AA%E5%BB%BA%E5%BA%94%E7%94%A8/
    def send(self, content=None, to_user="", to_party="", to_tag=""):
        token = self.get_access_token()
        if not token:
            print('Get token fault, please check the function:[get_access_token].')
            return False
        if not content:
            print('Please check content, content can not be None it must be str.')
            return False
        send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
        send_data = {
           "touser": to_user,
            "toparty": to_party,
            "totag": to_tag,
           "msgtype": "text",
           "agentid": 1000003,
           "text": {
               "content": content
           },
           "safe": 0
        }
        json_data = json.dumps(send_data).encode('utf-8')
        req = request.Request(url=send_url, data=json_data)
        res = request.urlopen(req)
        res_data = res.read()
        res_dict = json.loads(res_data.decode('utf-8'))
        print('Send message response.')
        print(res_dict)
        return True if res_dict["errcode"] == 0 else print(res_dict)


# 测试调用
if __name__ == "__main__":
    # 初始化转换成对象
    bot = Alert()
    # 输入企业ID和发送文本消息的应用密钥
    bot.login(ID='123', SECRET='safadsfs')
    # send 可选参数还有 to_user="", to_party="", to_tag="" 默认是全员发送
    bot.send(content="今天天气好吗?")
    '''
    output:
        {'errcode': 0, 'errmsg': 'ok', 'invaliduser': ''}
    '''