#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import ssl
import time
import Queue
import urllib2
import hashlib
import urlparse
import threading


def main():
    global sourceReturnHeader, testedUrl

    testedUrl = 'http://www.renji.com/'  # URL
    testedIP = '180.168.200.206'  # 请求主机IP

    threading_num = 20  # 线程数目

    sourceReturnHeader = getCDNSource(testUrl=testedUrl)
    print sourceReturnHeader

    queue = Queue.Queue()
    for num in xrange((threading_num - 1)):
        t = ThreadFuzzingHost(queue)
        t.setDaemon(True)
        t.start()

    testedIPTmp = '.'.join(testedIP.split('.')[:-1])
    for line in xrange(1, 255):
        hostIP = '{0}://{1}.{2}'.format(parseUrl(UrlAddress=testedUrl, target='SCHEME'), testedIPTmp,
                                        line)
        queue.put(hostIP)

    queue.join()


def getCDNSource(testUrl):
    sendHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    }
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        req = urllib2.Request(testUrl, headers=sendHeaders)
        r = urllib2.urlopen(req, timeout=5)
        html = r.read()
        r.close()
        receive_header = r.info()
        returnHeader = parseHttpHeader(httpHeader=receive_header)
        returnHeader['md5'] = getMd5(content=html)
        return returnHeader
    except:
        time.sleep(3)
        print 'reconnecting...'
        getCDNSource(testUrl)


def parseUrl(UrlAddress, target=''):
    if not UrlAddress.lower().startswith('http'):
        UrlAddress = 'http://' + UrlAddress
    parsedTuple = urlparse.urlparse(UrlAddress)
    if target.upper() == 'HOST':
        return parsedTuple.netloc.split(':')[0]
    elif target.upper() == 'SCHEME':
        return parsedTuple.scheme
    else:
        return parsedTuple.scheme + '://' + parsedTuple.netloc


def getMd5(content):
    return hashlib.md5(content).hexdigest()


def parseHttpHeader(httpHeader):
    httpHeaderDict = {}
    if httpHeader:
        for line in str(httpHeader).split('\r\n'):
            if line:
                singleData = line.split(':')
                headerStr = singleData[0]
                dataStr = ''.join(singleData[1:]).strip()
                httpHeaderDict[headerStr] = dataStr
    return httpHeaderDict


class ThreadFuzzingHost(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.timeout = 5  # 超时设置
        self.queue = queue
        self.Found = False  # 找到标识
        self.testedUrl = testedUrl

    def run(self):
        while True:
            Urlstr = self.queue.get()  # 找到了也要耗尽队列
            if not self.Found:  # 没有结果接着找
                self.FuzzingHost(RequestIP=Urlstr)
            self.queue.task_done()

    def FuzzingHost(self, RequestIP):
        sendHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'host': parseUrl(self.testedUrl, target='HOST')
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            # print RequestIP
            req = urllib2.Request(RequestIP, headers=sendHeaders)
            r = urllib2.urlopen(req, timeout=self.timeout)
            html = r.read()
            r.close()
            receive_header = r.info()
            returnHeader = parseHttpHeader(httpHeader=receive_header)
            returnHeader['md5'] = getMd5(content=html)
            if self.MatchHeader(httpReturnHeader=returnHeader):
                print 'Found Address:\t{0}\t{1}'.format(sendHeaders['host'], RequestIP)
        except:
            pass

    def MatchHeader(self, httpReturnHeader):  # 暂时先通过内容的MD5进行精确对比
        if httpReturnHeader:
            if httpReturnHeader['md5'] == sourceReturnHeader['md5'] and sourceReturnHeader['md5']:
                self.Found = True
                print httpReturnHeader
                return True


if __name__ == '__main__':
    main()

'''
➜  MyProjects python NewFuzzingHost.py
Found Address:	www.iiii.com	http://180.18.00.206
'''
