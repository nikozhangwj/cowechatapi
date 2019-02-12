# CoropWechatSendMsgAPI
调用企业微信API接口发送消息给指定用户
**文本消息例子:**

```python
from cowechat_api import CoWechatAPI

bot = CoWechatAPI()
bot.login(ID='123', SECRET='safadsfs')
bot.send(to_user="USER_NAME", msg_type="text", content="今天天气好吗?")
```

**文件消息例子:**

```python
from cowechat_api import CoWechatAPI

bot = CoWechatAPI()
bot.login(ID='123', SECRET='safadsfs')
bot.send(to_user="USER_NAME", msg_type="file", media_id="MEDIA_ID")
```

**图片消息例子:**
```python
from cowechat_api import CoWechatAPI

bot = CoWechatAPI()
bot.login(ID='123', SECRET='safadsfs')
bot.send(to_user="USER_NAME", msg_type="image", media_id="MEDIA_ID")
```

## media_id的获取方法是通过API的upload上传临时素材得到的，临时素材有效期为两天。 ##

**上传临时素材例子:**
```python
from cowechat_api import CoWechatAPI

bot = CoWechatAPI()
bot.login(ID='123', SECRET='safadsfs')
bot.upload(filetype="image", fileurl="FILE_PATH")
```
