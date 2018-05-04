#!/usr/bin/env python
# -*- coding: utf_8 -*-
# author: Tea

import os
import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def main():
    print nmapVul(sys.argv[1])


def nmapVul(xmlPath):
    if not os.path.exists(xmlPath):
        raise Exception('Xml file is not exists..')
    nmapXmlResult = list()
    try:
        tree = ET.ElementTree(file=xmlPath)
    except:
        return nmapXmlResult
    for dhost in tree.findall('host'):
        upStatus = ''
        host = dhost.find('address').get('addr')
        singleNmapDict = dict.fromkeys([host], [])
        for _host in dhost.findall('status'):
            upStatus = _host.get('state')
        if upStatus != 'up':
            return nmapXmlResult
        for _ports in dhost.findall('hostscript'):
            title, state, CVE = '', '', ''
            if _ports.find('script/table'):
                CVE = _ports.find('script/table').get('key')
            for _elem in _ports.findall('script/table/elem'):
                if (_elem.get('key') == 'state') and _elem.text != 'VULNERABLE':
                    return singleNmapDict
                if _elem.get('key') == 'title':
                    title = _elem.text
                    print host
            tmpNmapDict = {'state': 'VULNERABLE', 'title': title, 'CVE': CVE}
            if tmpNmapDict.get('CVE') or tmpNmapDict.get('title'):
                singleNmapDict[host].append(tmpNmapDict)
        if singleNmapDict[host]:
            nmapXmlResult.append(singleNmapDict)
    return nmapXmlResult


if __name__ == '__main__':
    main()
