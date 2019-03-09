
import time
import hashlib
import os
import sys
import requests

#def command(action, username='', password=''):
#    if action == 'login':
#        return 'curl -d action=login -d username=' + username + ' -d password=' + password + ' -d ac_id=1 net.tsinghua.edu.cn/do_login.php'
#    elif antion == 'logout':
#        return 'curl -d action=logout net.tsinghua.edu.cn/do_login.php'

#if len(sys.argv) < 3:
#    print('Incorrect argument number!')
#    exit()

#username = sys.argv[1]
#password = sys.argv[2]

username = 'abcdef'
password = '123456'
password = '{MD5_HEX}' + hashlib.md5(password.encode('utf-8')).hexdigest()

while True:
    f = open('log.txt', 'a')
    try:
        r = requests.post('http://net.tsinghua.edu.cn/do_login.php',
                          data={'action': 'login', 'username': username, 'password': password, 'ac_id': '1'})
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + r.text + '\n')
    except Exception as e:
        print(e)
    f.close()
    time.sleep(10)
