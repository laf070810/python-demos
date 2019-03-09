import requests
import itchat
from itchat.content import *


@itchat.msg_register(TEXT)
def tuling_reply(msg):
    if msg.user['RemarkName'] == '冯博伦':
        response = get_response(msg['Text'])

        try:
            if response['code'] == 100000:
                reply = response['text']
            elif response['code'] == 200000:
                reply = response['text'] + '：' + response['url']
            elif response['code'] == 302000:
                reply = response['text'] + '\n\n'
                for news in response['list']:
                    reply += news['article'] + '\n' + news['detailurl'] + '\n\n'
            elif response['code'] == 308000:
                reply = response['text'] + '\n\n'
                for dish in response['list']:
                    reply += dish['name'] + '：\n' + dish['info'] + '\n' + dish['detailurl'] + '\n\n'
            else:
                reply = '我收到了：' + msg['Text']
        except:
            reply = '我收到了：' + msg['Text']

        return reply


def get_response(msg: str) -> dict:
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': 'c3f875b621894457a6b32276d9a3c1c9',
        'info': msg,
        'userid': 'laf-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


itchat.auto_login(enableCmdQR=False, hotReload=False)
itchat.run()

# print(get_response('我想看新闻'))
