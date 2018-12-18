# CoropWechatSendMsgAPI
调用企业微信API接口发送消息给指定用户
**例子:**
(```)
import Alert
# 初始化转换成对象
bot = Alert()
# 输入企业ID和发送文本消息的应用密钥
bot.login(ID='123', SECRET='safadsfs')
# send 可选参数还有 to_user="", to_party="", to_tag="" 默认是全员发送
bot.send(content="今天天气好吗?")
(```)
------
output:
    {'errcode': 0, 'errmsg': 'ok', 'invaliduser': ''}
------
