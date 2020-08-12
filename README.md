# CoropWechatSendMsgAPI
目前这个工具需要使用到python3和requests模块

## 安装依赖
## pip安装 ##
```shell script
pip3 install -r requirements.txt
```

## 通过调用API接口发送消息
调用企业微信API接口发送消息给指定用户
**文本消息例子:**

```python
from cowechatapi.cowechat_api import CoWechatAPI

bot = CoWechatAPI(coid="your_company_id", secret="your_app_secret",agentid=1000001)
bot.send(to_user="USER_NAME", msg_type="text", content="今天天气好吗?")
```

**文件消息例子:**

```python
from cowechatapi.cowechat_api import CoWechatAPI

bot = CoWechatAPI(coid="your_company_id", secret="your_app_secret",agentid=1000001)
bot.send(to_user="USER_NAME", msg_type="file", media_id="MEDIA_ID")
```

**图片消息例子:**
```python
from cowechatapi.cowechat_api import CoWechatAPI

bot = CoWechatAPI(coid="your_company_id", secret="your_app_secret",agentid=1000001)
bot.send(to_user="USER_NAME", msg_type="image", media_id="MEDIA_ID")
```

## media_id的获取方法是通过API的upload上传临时素材得到的，临时素材有效期为两天。 ##

**上传临时素材例子:**
```python
from cowechatapi.cowechat_api import CoWechatAPI

bot = CoWechatAPI(coid="your_company_id", secret="your_app_secret",agentid=1000001)
bot.upload(filetype="image", fileurl="FILE_PATH")
```

## 通过命令行方式发送消息

```shell script
# 安装工具
git clone https://github.com/nikozhangwj/CoropWechatSendMsgAPI.git
mv CoropWechatSendMsgAPI /usr/local/cowechatApi
chmod +x /usr/local/cowechatApi/cowechat
ln -s /usr/local/cowechatApi/cowechat /usr/local/bin/cowechat
# 发送文本消息
cowechat -i [your_company_id] -s [your_app_secret] -a [your_agentid] -m text -c "content" --user [USER_NAME]
# 发送图片消息
cowechat -i [your_company_id] -s [your_app_secret] -a [your_agentid] -m image --media [media_id] --user [USER_NAME]
```
