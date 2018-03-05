#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup


def main():
    getAllList()


def getAllList():
    pageCount = 82
    urlTmp = 'http://www.mmxyz.net/?action=ajax_post&pag='
    for num in reversed(range(1, pageCount)):
        pageUrl = '{0}{1}'.format(urlTmp, num)
        getTopic(pageUrl)


def getTopic(pageUrl):
    # pageUrl = 'http://www.mmxyz.net/?action=ajax_post&pag=81'
    content = picRequest(pageUrl)
    bs = BeautifulSoup(content, 'lxml', from_encoding='utf8')
    allResult = bs.find_all('a', class_='inimg')
    for line in allResult:
        print '{0} {1}'.format(line.get('href'), line.get('title').encode('gbk'))


def picRequest(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    try:
        return requests.get(url, headers=headers).content
    except:
        time.sleep(0.5)
        print 'Re Request...'
        return requests.get(url, headers=headers).content


if __name__ == '__main__':
    main()
