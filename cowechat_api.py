# !/usr/bin/env python
# encoding: utf-8
# author: niko.zhang
# py_ver: py3

"""
first version
调用企业微信消息接口发送消息
可以指定某个用户、某个部门或者某个标签内的所有人员
初始化后需要调用login功能输入企业ID和消息应用密钥
密钥需要现在企业微信后台建立应用后才能获取
该代码需要在python3下的环境执行，不然会报消息类型错误
20190212 version
重构代码
增加上传临时素材功能
增加发送的消息类型 text image file voice video
增加简易日志输出
"""

import os
import json
import requests
import logging
from urllib import request
from datetime import datetime


class CoWechatAPI(object):

    LOG_DATE = datetime.now()
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_FILENAME = 'CWAPI.{}.log'.format(LOG_DATE.strftime("%Y%m%d"))
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    def __init__(self):
        # 设置企业微信的coropid和corpsecret, cache用来缓存token
        self.ID = ''
        self.SECRET = ''
        self.agentid = 1000001
        self.cache = os.path.join(os.getcwd(), '.token_cache')
        # 重试次数
        self.retry_count = 5

    # 企业微信的coropid和corpsecret写死的话不用执行login
    def login(self, ID, SECRET, agentid):
        if not ID and not SECRET:
            logging.error('Please input valid ID and SECRET.')
            return False
        self.ID = ID
        self.SECRET = SECRET
        self.agentid = agentid
        return True

    # 用来保存token到缓存文件
    def save_token(self, token_dict):
        token_dict['date'] = datetime.strftime(datetime.now(), "%Y-%m-%d %H%M%S")
        with open(self.cache, 'wt') as fhandler:
            fhandler.write(json.dumps(token_dict, indent=4))

    # 通过时间判断token是否有效，token有效时间为两个小时
    def token_valid(self):
        if not os.path.exists(self.cache):
            logging.info('token_cache has not found.')
            return False
        with open(self.cache, 'rt') as fhandler:
            data = json.loads(fhandler.read())
            if data['errmsg'] != 'ok':
                logging.error('Cache has no token but error message: ' + data['errmsg'])
                return False
            else:
                logging.info('Cache has no error message.')
            token_date = data['date']
            usetime = (datetime.now() - datetime.strptime(token_date, "%Y-%m-%d %H%M%S")).seconds
            if usetime >= 7200:
                logging.info('Cache token is overtime, get new token from url.')
                return False
            else:
                logging.info('Cache token is valid, get token from cache.')
                return True

    # 通过企业微信API重新获取token
    def get_access_token_url(self):
        token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(self.ID,
                                                                                                  self.SECRET)
        try:
            res = request.urlopen(token_url)
            # print(res.read())
        except BaseException as error:
            print(error)
            return False
        res_data = res.read()
        res_dict = json.loads(res_data.decode('utf-8'))
        logging.info('Get token from token_url.')
        logging.debug(res_dict)
        try:
            res_dict.get('access_token')
        except KeyError as error:
            logging.error(error)
            return False
        self.save_token(res_dict)
        return res_dict['access_token']

    # 通过缓存文件获取token
    def get_access_token_cache(self):
        with open(self.cache, 'rt') as fhandler:
            data = json.loads(fhandler.read())
            logging.info('Get token from cache.')
            logging.debug(data)
            try:
                return data['access_token']
            except KeyError as error:
                logging.error(error)
                return False

    # 获取token功能
    def get_access_token(self):
        if self.token_valid():
            return self.get_access_token_cache()
        else:
            return self.get_access_token_url()

    # 消息前置: 消息分类构造再传入发送方法
    def send(self, msg_type=None, to_user="", to_party="", to_tag="", content=None, media_id=None):

        send_data = {
           "touser": to_user,
            "toparty": to_party,
            "totag": to_tag,
           "msgtype": msg_type,
           "agentid": self.agentid,
           "safe": 0
        }

        if not msg_type:
            logging.error('msg_type can not be None.')
            return False

        if msg_type == "text":
            send_data["text"] = {
               "content": content
            }
            logging.info('Start send {} message.'.format(msg_type))
            logging.debug(send_data)
        elif msg_type == "image" and media_id:
            send_data["image"] = {
                "media_id": media_id
            }
            logging.info('Start send {} message.'.format(msg_type))
            logging.debug(send_data)
        elif msg_type == "voice" and media_id:
            send_data["voice"] = {
                "media_id": media_id
            }
            logging.info('Start send {} message.'.format(msg_type))
            logging.debug(send_data)
        elif msg_type == "video" and media_id:
            send_data["video"] = {
                "media_id": media_id,
                "title": "Title",
                "description": "Description"
            }
            logging.info('Start send {} message.'.format(msg_type))
            logging.debug(send_data)
        elif msg_type == "file" and media_id:
            send_data["file"] = {
                "media_id": media_id
            }
            logging.info('Start send {} message.'.format(msg_type))
            logging.debug(send_data)
        else:
            logging.error("data error")
            return False

        count = 0
        while count < self.retry_count:
            if self.send_util(send_data=send_data):
                return True
            count += 1
        return False

    # 消息发送方法
    def send_util(self, send_data):
        token = self.get_access_token()
        send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
        json_data = json.dumps(send_data).encode('utf-8')
        req = request.Request(url=send_url, data=json_data)
        res = request.urlopen(req)
        res_data = res.read()
        res_dict = json.loads(res_data.decode('utf-8'))
        if res_dict["errcode"] == 0:
            # print('Send message response.')
            logging.info('Send message response: ' + res_dict["errmsg"])
            return True
        else:
            logging.error('Send message error response: ' + res_dict)
            return False

    # 上传临时素材
    def upload(self, filetype, fileurl):
        if not filetype or not fileurl:
            logging.error("Missing args error")
        token = self.get_access_token()
        upload_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}".format(token, filetype)
        files = {
            'file': open(fileurl, 'rb')
        }
        response = requests.post(url=upload_url, files=files)
        logging.info(response.status_code)
        logging.info(response.text)
        return response.text
