# -*- coding: utf-8 -*-
import pycurl
import urllib
import re

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

postHeader = [
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding: gzip, deflate',
    'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Cache-Control: max-age=0',
    'Connection: keep-alive',
    'Content-Length: 45',
    'Host: uems.sysu.edu.cn',
    'Origin: http://uems.sysu.edu.cn',
    'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
    'Content-Type: application/x-www-form-urlencoded',
    ]

getHeader = [
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding: gzip, deflate, sdch',
    'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Connection: keep-alive',
    'Host: uems.sysu.edu.cn',
    'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
]

class Jwxt:
    def __init__(self):
        self.cookiePattern = re.compile(r'(?<=Set-Cookie:\ )(.+?)(?=;)')
        self.cookie = None
        self.urls = {
            'login': 'http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do',
            'cookie': 'http://uems.sysu.edu.cn/jwxt/',
        }

    def getData(self, url, headerCallback, callback):
        connect = pycurl.Curl()
        connect.setopt(connect.URL, url)
        connect.setopt(connect.HTTPHEADER, getHeader)
        connect.setopt(connect.HEADERFUNCTION, headerCallback)
        connect.setopt(connect.WRITEFUNCTION, callback)
        connect.perform()
        connect.close()

    def postData(self, url, data, headerCallback, callback):
        postData = urllib.urlencode(data)
        connect = pycurl.Curl()
        connect.setopt(connect.URL, url)
        connect.setopt(connect.FOLLOWLOCATION, True)
        connect.setopt(connect.POST, True)
        connect.setopt(connect.POSTFIELDS, postData)
        connect.setopt(connect.COOKIE, self.cookie)
        connect.setopt(connect.HEADERFUNCTION, headerCallback)
        connect.setopt(connect.WRITEFUNCTION, callback)
        connect.setopt(connect.HTTPHEADER, postHeader)
        connect.perform()
        connect.close()

    def passHeader(self, headerLine):
        pass

    def passWrite(self, data):
        pass

    def cookieHeaderFunction(self, headerLine):
        field = headerLine.split(':')[0]
        if field == 'Set-Cookie':
            cookie = self.cookiePattern.search(headerLine).group()
            self.cookie = cookie
            print self.cookie

    def loginWriteFunction(self, data):
        print data

    def getCookie(self):
        self.getData(self.urls['cookie'],
            self.cookieHeaderFunction, self.passWrite)

    def login(self, username, password):
        if self.cookie is None:
            self.getCookie()
        self.postData(self.urls['login'], {
            'j_username': username,
            'j_password': password,
            }, self.passHeader, self.passWrite)

if __name__ == '__main__':
    jwxt = Jwxt()
    jwxt.login('12330071', '33519000091533')

