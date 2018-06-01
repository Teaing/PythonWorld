#!/usr/bin/env python
# -*- coding: utf_8 -*-
# author: Tea

import Queue
import socket
import requests
import threading

StatusCode, ContentLength = '', ''


def main():
    global StatusCode, ContentLength
    StatusCode, ContentLength = onceRequest()  # 请求一次有CDN的数据,比较http状态码以及内容长度

    testedIP = '10.20.195.69'  # 测试的IP地址段
    threading_num = 10
    queue = Queue.Queue()
    testedIPTmp = '.'.join(testedIP.split('.')[:-1])

    for num in xrange((threading_num - 1)):
        t = ThreadGetHost(queue)
        t.setDaemon(True)
        t.start()

    for line in xrange(1, 255):
        hostIP = '{0}.{1}'.format(testedIPTmp, line)
        queue.put(hostIP)

    queue.join()


def onceRequest():
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0',
              'Cache-Control': 'no-cache'}
    requestAction = requests.get('http://www.xxxxx.gov.cn/', headers=header)  # 测试的网站地址
    StatusCode = requestAction.status_code
    ContentLength = requestAction.headers.get('Content-Length')
    return StatusCode, ContentLength


class ThreadGetHost(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.testedUrl = 'www.xxxxx.gov.cn'  # 测试的网站地址
        self.getData = 'GET %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0\r\nAccept: */*\r\n\r\n'

    def run(self):
        while True:
            host = self.queue.get()
            self.requestHost(host)
            self.queue.task_done()

    def requestHost(self, ip, port=80):
        # global StatusCode, ContentLength
        socketMe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketMe.settimeout(3)
        try:
            socketMe.connect((ip, port))
            socketMe.settimeout(None)
            socketMe.send(self.getData % ('/', self.testedUrl + ':' + port.__str__()))
            buffStr = socketMe.recv(1024)
            httpHeaderDict = self.parseHttpHeader(buffStr)
            print 'Host Tested\t%s:%d' % (ip, port)
            # print httpHeaderDict
            if httpHeaderDict.get('StatusCode') == StatusCode and httpHeaderDict.get('Content-Length') == ContentLength:
                print 'Good Luck!Found Host:\t%s:%d' % (ip, port)
            socketMe.close()
        except Exception, e:
            pass

    def parseHttpHeader(self, httpData):
        if httpData.startswith('HTTP'):
            httpHeader = {}
            headerData = httpData.split("\r\n\r\n")[0]
            headerDataSplit = headerData.split('\r\n')
            statusCode = headerDataSplit[0].split(' ')[1]
            httpHeader['StatusCode'] = statusCode
            for line in range(1, len(headerDataSplit)):
                lineData = headerDataSplit[line]
                singleData = lineData.split(':')
                headerStr = singleData[0]
                dataStr = ''.join(singleData[1:])
                httpHeader[headerStr] = dataStr
            return httpHeader


if __name__ == '__main__':
    main()
