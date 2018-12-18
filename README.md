# CoropWechatSendMsgAPI
调用企业微信API接口发送消息给指定用户
**例子:**

(```)
import Alert

bot = Alert()
bot.login(ID='123', SECRET='safadsfs')
bot.send(content="今天天气好吗?")
(```)

------
output:
    {'errcode': 0, 'errmsg': 'ok', 'invaliduser': ''}
------
