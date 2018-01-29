#!/usr/bin/env python
# -*- coding: utf_8 -*-
# author: Tea

import sys
import time
import logging
import smtplib
import platform
import subprocess
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', )


def main():
    systemVer = getSystemVersion()
    monitorAction(systemVer)


def monitorAction(systemVersion):
    processList = infoConfig().get('process')
    if not processList:
        logging.warning('process list is empty!')
        sys.exit()
    logging.info('monitor process count: %d' % len(processList))
    loopTime = loopStatus()
    if loopTime:
        while True:
            loopAction(systemVersion, processList)
            time.sleep(loopTime * 60)
    else:
        loopAction(systemVersion, processList)


def loopAction(systemVersion, processList):
    if systemVersion.startswith('Windows'):
        windowsMonitor(processList)
    elif systemVersion.startswith('Linux'):
        linuxMonitor(processList)
    else:
        sys.exit('What The Fuck...')


def windowsMonitor(processList):
    # mirror_code = ''.join(['TASKLIST.exe /V /NH /FO csv /FI "IMAGENAME eq ',process_name,'"'])  # pass or wmic?
    try:
        # ['TASKLIST.exe', '/V', '/NH', '/FO', 'CSV']
        p = subprocess.Popen(['TASKLIST.exe', '/V', '/NH', '/FO', 'CSV', '/FI', 'STATUS eq running'], bufsize=0,
                             stdout=subprocess.PIPE)
    except Exception, e:
        pass
    monitorOutput = p.communicate()[0]
    monitorProcessList = monitorOutput.split('\r\n')
    runningStatus = False
    if monitorProcessList:
        for _process in processList:
            for monitorOneList in monitorProcessList:
                processOne = monitorOneList.split(',')
                processName = processOne[0][1:-1]  # 进程名称
                processDes = processOne[-1]  # 进程说明
                if _process == processName:
                    runningStatus = True
                    break
                elif _process in processDes:
                    runningStatus = True
                    break
            checkStautsSendInfo(_process, runningStatus)


def linuxMonitor(processList):
    for _process in processList:
        try:
            processExec = subprocess.Popen('ps -ef|grep ' + _process + '|grep -v \'grep \'',
                                           shell=True, bufsize=0,
                                           stdout=subprocess.PIPE)
        except Exception, e:
            pass
        monitorOutput = processExec.communicate()[0]
        runningStatus = True if monitorOutput else False
        checkStautsSendInfo(_process, runningStatus)


def checkStautsSendInfo(processName, runningStatus):
    checkLiveStatus = infoConfig().get('checkLiveStatus')
    if checkLiveStatus:  # True: 进程不管是活的还是死的都发警告信息
        if runningStatus:
            messageContent(processName)  # 进程活着
        else:
            messageContent(processName, False)  # 进程死了
    else:  # False: 进程死了发送警告信息,只发送一次,活着没有动作
        if runningStatus is False:
            messageContent(processName, False)  # 进程死了
            sys.exit('Game Over!')


def messageContent(processName, runningStatus=True):
    nowTime = getNow()
    if runningStatus:
        message = ''.join(['Alive, Process: ', processName, '\n', nowTime])
    else:
        message = ''.join(['Death, Process: ', processName, '\n', nowTime])
    WarningSend.mailSend('Warning', message)


def getNow():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))


def loopStatus():
    intervalTime = int(infoConfig().get('intervalTime'))
    if intervalTime >= 1:
        return intervalTime
    else:
        return False


def getSystemVersion():
    systemVer = platform.system()
    logging.info('current system: %s' % systemVer)
    return systemVer


def infoConfig():
    configDict = dict(
        process=['git-svn', 'main.py'],  # 要监控的进程列表
        mobile=['13666666666'],  # 手机号码,用于接收警告信息
        email=['13666666666@139.com'],  # 邮箱,用于接收警告信息
        intervalTime=0,  # 检查频率,值如果大于等于1分钟，默认启用脚本内循环
        checkLiveStatus=True  # False: 进程死了发送警告信息,只发送一次,活着没有动作 True: 进程不管是活的还是死的都发警告信息
    )
    return configDict


class WarningSend:

    @staticmethod
    def mailSend(sub, content):
        mailAddress = infoConfig().get('email')
        mailHost = 'smtp.139.com'
        mailUserName = '139139139'
        mailPassWord = '139139139'
        mailPostfix = '139.com'
        if not mailAddress:
            logging.warning('mail address is empty!')
            return False
        me = "admin<" + mailUserName + "@" + mailPostfix + ">"
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(mailAddress)
        try:
            server = smtplib.SMTP()
            server.connect(mailHost)
            server.login(mailUserName, mailPassWord)
            server.sendmail(me, mailAddress, msg.as_string())
            server.close()
        except Exception, e:
            logging.warning('mail send failure!!!')
            logging.warning(str(e))

    @staticmethod
    def smsSend(content):
        mobile = infoConfig().get('mobile')
        if not mobile:
            logging.warning('mobile number is empty!')
        pass  # 发送短信后续代码


if __name__ == '__main__':
    main()
