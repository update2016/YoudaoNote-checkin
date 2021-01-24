import requests
import json
import time
import urllib3
import os
import hashlib

urllib3.disable_warnings()


username = os.environ['USERNAME']
password = os.environ['PASSWORD']


def checkin(username: str, password: str):
    login_url = 'https://note.youdao.com/login/acc/urs/verify/check?app=web&product=YNOTE&tp=urstoken&cf=6&fr=1&systemName=&deviceType=&ru=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&er=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&vcode=&systemName=mac&deviceType=MacPC&timestamp=1611466345699'
    checkin_url = 'http://note.youdao.com/yws/mapi/user?method=checkin'

    m = hashlib.md5()
    m.update(password.encode('utf8'))

    parame = {
        'username': username,
        'password': m.hexdigest(),
    }

    s = requests.Session()
    # 登录
    s.post(url=login_url, data=parame, verify=False)

    # 签到
    r = s.post(url=checkin_url)
    print(r.text)
    if r.status_code == 200:
        info = json.loads(r.text)
        total = info['total'] / 1048576
        space = info['space'] / 1048576
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info['time'] / 1000))

        print('{} | 这次签到获得：{} M | 总共获得：{} M | 签到时间：{}'.format(username, space, total, t))


if __name__ == "__main__":
    checkin(username, password)
