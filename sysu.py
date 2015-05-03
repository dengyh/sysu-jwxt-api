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
    # 'Accept-Encoding: gzip, deflate',
    'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Cache-Control: max-age=0',
    'Connection: keep-alive',
    # 'Content-Length: 45',
    'Host: uems.sysu.edu.cn',
    'Origin: http://uems.sysu.edu.cn',
    'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
    'Content-Type: application/x-www-form-urlencoded',
    ]

getHeader = [
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding: gzip, deflate, sdch',
    'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Connection: keep-alive',
    'Host: uems.sysu.edu.cn',
    'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
]

cookiePattern = re.compile(r'(?<=Set-Cookie:\ )(.+?)(?=;)')

buffer = None

class Jwxt:
    def __init__(self, username, password):
        self.cookie = None
        self.username = username
        self.password = password
        self.urls = {
            'login': 'http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do',
            'cookie': 'http://uems.sysu.edu.cn/jwxt/',
            'score': 'http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjxAction.action?method=getKccjList',
            'credit': 'http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjxAction.action?method=getAllJd',
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
        try:
            data = urllib.urlencode(data)
        except:
            pass
        connect = pycurl.Curl()
        connect.setopt(connect.URL, url)
        connect.setopt(connect.FOLLOWLOCATION, True)
        connect.setopt(connect.POST, True)
        connect.setopt(connect.POSTFIELDS, data)
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

    def debugWrite(self, data):
        buffer.write(data)

    def cookieHeaderFunction(self, headerLine):
        field = headerLine.split(':')[0]
        if field == 'Set-Cookie':
            cookie = cookiePattern.search(headerLine).group()
            self.cookie = cookie
            print self.cookie

    def getCookie(self):
        self.getData(self.urls['cookie'],
            self.cookieHeaderFunction, self.passWrite)

    def login(self):
        if self.cookie is None:
            self.getCookie()
        self.postData(self.urls['login'], {
            'j_username': self.username,
            'j_password': self.password,
            }, self.passHeader, self.passWrite)

    def getScore(self):
        if self.cookie is None:
            self.login()
        data = '''{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{kccjStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"kccjStore",pageNumber:1,pageSize:10,recordCount:0,rowSetName:"pojo_com.neusoft.education.sysu.xscj.xscjcx.model.KccjModel",order:"t.xn, t.xq, t.kch, t.bzw"}},parameters:{"kccjStore-params": [{"name": "Filter_t.pylbm_0.6220199986403405", "type": "String", "value": "'01'", "condition": " = ", "property": "t.pylbm"}, {"name": "Filter_t.xn_0.17289099200582425", "type": "String", "value": "'2012-2013'", "condition": " = ", "property": "t.xn"}, {"name": "Filter_t.xq_0.5098009446703891", "type": "String", "value": "'1'", "condition": " = ", "property": "t.xq"}], "args": ["student"]}}}'''
        self.postData(self.urls['score'], data, self.passHeader, buffer.write)

    def getCredit(self):
        if self.cookie is None:
            self.login()
        data = '''{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{jdStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"jdStore",pageNumber:1,pageSize:2147483647,recordCount:0,rowSetName:"pojo_com.neusoft.education.sysu.djks.ksgl.model.TwoColumnModel"}},parameters:{"args": ["12330071", "2012-2013", "1", ""]}}}'''
        self.postData(self.urls['credit'], data, self.passHeader, buffer.write)

if __name__ == '__main__':
    buffer = StringIO()
    jwxt = Jwxt('12330071', '33519000091533')
    jwxt.getScore()
    print buffer.getvalue()