# !/usr/bin/env python3
# encoding: utf-8
# author: niko.zhang
# py_ver: py3

"""
调用企业微信消息接口发送消息
可以指定某个用户、某个部门或者某个标签内的所有人员
初始化对象需要输入企业ID,应用Secret和AgentId
密钥需要现在企业微信后台建立应用后才能获取
该代码需要在python3下的环境执行，不然会报消息类型错误
UPDATE: 20200812
"""

import os
import json
import requests
import logging
from logging import handlers
import platform
from datetime import datetime


class CoWechatAPI(object):

    def __init__(self, coid, secret, agentid, retry=5, logger=None):
        # init Object
        # 初始化临时目录
        self._init_tmp_folder()
        # 可以传入自定义的logger
        self._init_logger(logger)
        # 初始化对象需要输入企业微信的company_id、应用的secret和agentid
        self.ID = coid
        self.SECRET = secret
        self.agentid = agentid
        # access_token
        self.token = ""
        # 缓存access_token的文件
        self.cache = os.path.join(self.tmp_folder, '.token_cache')
        # 请求重试次数
        self.retry_count = retry
        self.login()

    def _init_tmp_folder(self):
        # 通过环境变量获取系统临时目录作为缓存文件的存放位置
        if platform.system() == "Linux":
            self.tmp_folder = os.environ.get('HOME', '/tmp')
        elif platform.system() == "Windows":
            # 如果环境变量中没有临时目录则选择当前目录作为缓存目录
            self.tmp_folder = os.environ.get('TMP') or os.environ.get('HOMEPATH') or os.getcwd()
        else:
            self.tmp_folder = os.getcwd()

    def _init_logger(self, logger):
        if not logger:
            LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"
            DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
            formatter = logging.Formatter(LOG_FORMAT)
            formatter.datefmt = DATE_FORMAT
            # 输出屏幕
            stream_formatter = logging.Formatter("%(message)s")
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(stream_formatter)
            stream_handler.setLevel(logging.ERROR)
            # 输出文件
            api_handler = handlers.TimedRotatingFileHandler(
                os.path.join(self.tmp_folder, 'cowechatapi.log'),
                when='w0',
                backupCount=7
            )
            api_handler.setFormatter(formatter)
            logging.basicConfig(
                level=logging.INFO,
                format=LOG_FORMAT,
                datefmt=DATE_FORMAT
            )
            logger = logging.getLogger(__name__)
            logger.addHandler(api_handler)
            logger.addHandler(stream_handler)
        self.logger = logger

    # 登录功能
    def login(self):
        if not self.ID and not self.SECRET:
            self.logger.error('Please input valid ID and SECRET.')
            return False
        self.token = self.get_access_token()

    # 用来缓存token到本地文件
    def save_token(self, token_dict):
        token_dict['date'] = datetime.strftime(datetime.now(), "%Y-%m-%d %H%M%S")
        with open(self.cache, 'wt') as fhandler:
            fhandler.write(json.dumps(token_dict, indent=4))

    # 通过时间判断token是否有效，token有效时间为两个小时
    def token_valid(self):
        if not os.path.exists(self.cache):
            self.logger.info('token_cache has not found.')
            return False
        with open(self.cache, 'rt') as fhandler:
            data = json.loads(fhandler.read())
            if data['errmsg'] != 'ok':
                self.logger.error('Cache has no token but error message: ' + data['errmsg'])
                return False
            else:
                self.logger.info('Cache has no error message.')
            token_date = data['date']
            usetime = (datetime.now() - datetime.strptime(token_date, "%Y-%m-%d %H%M%S")).total_seconds()
            if usetime >= 7200:
                self.logger.info('Cache token is overtime, get new token from url.')
                return False
            else:
                self.logger.info('Cache token is valid, get token from cache.')
                return True

    # 通过企业微信API获取access_token
    def get_access_token_url(self):
        token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(self.ID,
                                                                                                  self.SECRET)
        try:
            res = requests.get(token_url)
        except BaseException as error:
            self.logger.exception(error)
            return False
        res_dict = res.json()
        self.logger.info('Get token from token_url.')
        self.logger.debug(res_dict)
        try:
            res_dict.get('access_token')
        except KeyError as error:
            self.logger.exception(error)
            return False
        self.save_token(res_dict)
        return res_dict['access_token']

    # 通过缓存文件获取access_token
    def get_access_token_cache(self):
        with open(self.cache, 'rt') as fhandler:
            data = json.loads(fhandler.read())
            self.logger.info('Get token from cache.')
            self.logger.debug(data)
            try:
                return data['access_token']
            except KeyError as error:
                self.logger.exception(error)
                return False

    # 获取access_token
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
            self.logger.error('msg_type can not be None.')
            raise Exception("msg_type can not be None.")

        if msg_type == "text":
            send_data["text"] = {
                "content": content
            }
            self.logger.info('Start send {} message:{}.'.format(msg_type, content))
            self.logger.debug(send_data)
        elif msg_type == "image" and media_id:
            send_data["image"] = {
                "media_id": media_id
            }
            self.logger.info('Start send {} message:{}.'.format(msg_type, media_id))
            self.logger.debug(send_data)
        elif msg_type == "voice" and media_id:
            send_data["voice"] = {
                "media_id": media_id
            }
            self.logger.info('Start send {} message:{}.'.format(msg_type, media_id))
            self.logger.debug(send_data)
        elif msg_type == "video" and media_id:
            send_data["video"] = {
                "media_id": media_id,
                "title": "Title",
                "description": "Description"
            }
            self.logger.info('Start send {} message:{}.'.format(msg_type, media_id))
            self.logger.debug(send_data)
        elif msg_type == "file" and media_id:
            send_data["file"] = {
                "media_id": media_id
            }
            self.logger.info('Start send {} message:{}.'.format(msg_type, media_id))
            self.logger.debug(send_data)
        else:
            _err_msg = "Message type:{} or arguments invalid, please check yourself.".format(msg_type)
            self.logger.error(_err_msg)
            raise Exception(_err_msg)

        count = 0
        while count < self.retry_count:
            if self._send_util(send_data=send_data):
                return True
            count += 1
        return False

    # 消息发送方法
    def _send_util(self, send_data):
        send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(self.token)
        res = requests.post(send_url, json=send_data)
        res_dict = res.json()
        self.logger.debug(res_dict)
        if res_dict["errcode"] == 0:
            self.logger.info('Send message response: ' + res_dict["errmsg"])
            return True
        else:
            self.logger.error('Send message error response: ' + res_dict["errmsg"])
            raise Exception(res_dict["errmsg"])

    # 上传临时素材
    def upload(self, filetype, fileurl):
        if not filetype or not fileurl:
            self.logger.error("Missing args error")
        token = self.get_access_token()
        upload_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}".format(token, filetype)
        files = {
            'file': open(fileurl, 'rb')
        }
        response = requests.post(url=upload_url, files=files)
        self.logger.info(response.status_code)
        self.logger.info(response.text)
        return response.text
