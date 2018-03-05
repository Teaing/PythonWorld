#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup


def main():
    getMainPage()
    url = 'http://www.mmxyz.net/rosi-2220/'
    getPicUrl(url)


def getPicUrl(contentUrl):
    getHrefUrl(contentUrl, 'dt', 'gallery-icon')


def picRequest(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    try:
        return requests.get(url, headers=headers).content
    except:
        time.sleep(0.5)
        print 'Re Request...'
        return requests.get(url, headers=headers).content


def getMainPage():
    url = 'http://www.mmxyz.net/'
    getHrefUrl(url, 'a', 'inimg')


def getHrefUrl(url, htmlTag, cssClass):
    content = picRequest(url)
    bs = BeautifulSoup(content, 'html.parser', from_encoding='gbk')
    print bs.title.string
    allResult = bs.find_all(htmlTag, class_=cssClass)
    if htmlTag == 'dt':
        for line in allResult:
            print line.a.get('href')
    else:
        for line in allResult:
            print line.get('href')


if __name__ == '__main__':
    main()
