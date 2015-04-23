# -*- coding: utf-8 -*-
import pycurl
import re
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

header = [
    'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding:gzip, deflate, sdch',
    'Accept-Language:en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Cache-Control:max-age=0',
    'Connection:keep-alive',
    'Host:uems.sysu.edu.cn',
    'User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'
    ]

class Jwxt:
    def __init__(self):
        self.cookiePattern = re.compile(r'(?<=Set-Cookie:\ )(.+?)(?=;)')
        self.cookie = None
        self.header = header

    def getData(self, url, headerCallback, callback):
        connect = pycurl.Curl()
        connect.setopt(connect.URL, url)
        connect.setopt(connect.HTTPHEADER, self.header)
        connect.setopt(connect.HEADERFUNCTION, headerCallback)
        connect.setopt(connect.WRITEFUNCTION, callback)
        connect.perform()
        connect.close()

    def addHeader(self, newLine):
        self.header.append(newLine)

    def passHeader(self, headerLine):
        pass

    def passWrite(self, data):
        pass

    def cookieHeaderFunction(self, headerLine):
        field = headerLine.split(':')[0]
        if field == 'Set-Cookie':
            cookie = self.cookiePattern.search(headerLine).group()
            self.cookie = cookie
            self.addHeader('Cookie: ' + self.cookie)

    def getCookie(self):
        self.getData('http://uems.sysu.edu.cn/jwxt/',
            self.cookieHeaderFunction, self.passWrite)

    

jwxt = Jwxt()
jwxt.getCookie()

