from flask import Flask
from flask import request
from flask import make_response
from threading import Thread
import itchat
from itchat.content import *
import os
import time
import shutil
import re
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
itchat_thread = None
login_flag = False
sched = None
name = sys.argv[1]
port = sys.argv[2]

# 文件临时存储页
rec_tmp_dir = os.path.join(os.getcwd(), 'tmp/')

# 存储数据的字典
rec_msg_dict = {}


@app.route('/anti_revoke_' + name, methods=['GET', 'POST'])
def reply():
    global itchat_thread

    if (itchat_thread is None) or (not itchat_thread.isAlive()):
        if os.path.exists('./QR.png'):
            os.remove('./QR.png')
        itchat_thread = Thread(target=run_itchat)
        itchat_thread.start()
        while not os.path.exists('./QR.png'):
            pass
        return '<pre>' + '请用微信扫描以下二维码并登录，确认已登录后请刷新此页面<br>' + '</pre>\n' + '<img src="/anti_revoke_' + name + '/QR.png"  alt="图片加载失败" />'
    elif not login_flag:
        return '<pre>' + '请用微信扫描以下二维码并登录，确认已登录后请刷新此页面<br>' + '</pre>\n' + '<img src="/anti_revoke_' + name + '/QR.png"  alt="图片加载失败" />'
    else:
        return '<pre>' + '自动回复已启动' + '</pre>\n'


@app.route('/anti_revoke_' + name + '/<string:filename>', methods=['GET'])
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


# 好友信息监听
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
    msg_id = msg['MsgId']
    msg_from_user = msg['User']['NickName']
    msg_content = ''
    # 收到信息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
    msg_create_time = msg['CreateTime']
    msg_type = msg['Type']

    if msg['Type'] == 'Text':
        msg_content = msg['Content']
    elif msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Attachment':
        msg_content = r"" + msg['FileName']
        msg['Text'](rec_tmp_dir + msg['FileName'])

    rec_msg_dict.update({
        msg_id: {
            'msg_from_user': msg_from_user,
            'msg_time_rec': msg_time_rec,
            'msg_create_time': msg_create_time,
            'msg_type': msg_type,
            'msg_content': msg_content
        }
    })
    print(msg)


# 群聊信息监听
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def information(msg):
    msg_id = msg['MsgId']
    msg_from_user = msg['ActualNickName']
    msg_content = ''
    # 收到信息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
    msg_create_time = msg['CreateTime']
    msg_type = msg['Type']

    if msg['Type'] == 'Text':
        msg_content = msg['Content']
    elif msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Attachment':
        msg_content = r"" + msg['FileName']
        msg['Text'](rec_tmp_dir + msg['FileName'])

    rec_msg_dict.update({
        msg_id: {
            'msg_from_user': msg_from_user,
            'msg_time_rec': msg_time_rec,
            'msg_create_time': msg_create_time,
            'msg_type': msg_type,
            'msg_content': msg_content
        }
    })
    print(msg)


@itchat.msg_register([NOTE], isFriendChat=True, isGroupChat=True)
def revoke_msg(msg):
    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = rec_msg_dict.get(old_msg_id, {})
        # 先发送一条文字信息
        itchat.send_msg(str(old_msg.get('msg_from_user') + "撤回了一条信息："
                            + old_msg.get('msg_content')), toUserName="filehelper")
        # 判断文msg_content是否存在，不存在说明可能是
        if os.path.exists(os.path.join(rec_tmp_dir, old_msg.get('msg_content'))):
            if old_msg.get('msg_type') == 'Picture':
                itchat.send_image(os.path.join(rec_tmp_dir, old_msg.get('msg_content')),
                                  toUserName="filehelper")
            elif old_msg.get('msg_type') == 'Video':
                itchat.send_video(os.path.join(rec_tmp_dir, old_msg.get('msg_content')),
                                  toUserName="filehelper")
            elif old_msg.get('msg_type') == 'Attachment' \
                    or old_msg.get('msg_type') == 'Recording':
                itchat.send_file(os.path.join(rec_tmp_dir, old_msg.get('msg_content')),
                                 toUserName="filehelper")
    print(msg)


def clear_cache():
    # 当前时间
    cur_time = time.time()
    # 遍历字典，如果有创建时间超过2分钟(120s)的记录，删除，非文本的话，连文件也删除
    for key in list(rec_msg_dict.keys()):
        if int(cur_time) - int(rec_msg_dict.get(key).get('msg_create_time')) > 120:
            if not rec_msg_dict.get(key).get('msg_type') == 'Text':
                file_path = os.path.join(rec_tmp_dir, rec_msg_dict.get(key).get('msg_content'))
                print(file_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
            rec_msg_dict.pop(key)


# 开始轮询任务
def start_schedule():
    sched.add_job(clear_cache, 'interval', minutes=2)
    sched.start()


# 退出停止所有任务并清空缓存文件夹
def after_logout():
    sched.shutdown()
    shutil.rmtree(rec_tmp_dir)


def run_itchat():
    global login_flag, sched

    sched = BlockingScheduler()
    if not os.path.exists(rec_tmp_dir):
        os.mkdir(rec_tmp_dir)
    itchat.auto_login(exitCallback=after_logout)
    login_flag = True
    itchat.run(blockThread=False)
    start_schedule()
    login_flag = False


if __name__ == '__main__':
    app.run(host='localhost', port=int(port))
