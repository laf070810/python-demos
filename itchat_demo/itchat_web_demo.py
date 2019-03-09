from flask import Flask
from flask import request
from flask import make_response
from itchat.content import *
from threading import Thread
import os
import requests
import itchat

app = Flask(__name__)
itchat_thread = None
login_flag = False


@app.route('/auto_reply_dep71', methods=['GET', 'POST'])
def reply():
    global itchat_thread

    if (itchat_thread is None) or (not itchat_thread.isAlive()):
        if os.path.exists('./QR.png'):
            os.remove('./QR.png')
        itchat_thread = Thread(target=run_itchat)
        itchat_thread.start()
        while not os.path.exists('./QR.png'):
            pass
        return '<pre>' + '请用微信扫描以下二维码并登录，确认已登录后请刷新此页面<br>' + '</pre>\n' + '<img src="/auto_reply_dep71/QR.png"  alt="图片加载失败" />'
    elif not login_flag:
        return '<pre>' + '请用微信扫描以下二维码并登录，确认已登录后请刷新此页面<br>' + '</pre>\n' + '<img src="/auto_reply_dep71/QR.png"  alt="图片加载失败" />'
    else:
        return '<pre>' + '自动回复已启动' + '</pre>\n'


@app.route('/auto_reply_dep71/<string:filename>', methods=['GET'])
def show_photo(filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join('./', filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass


@itchat.msg_register(TEXT)
def tuling_reply(msg):
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
        'userid': 'DEP71-robot',
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


def run_itchat():
    global login_flag

    itchat.auto_login()
    login_flag = True
    itchat.run()
    login_flag = False


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
