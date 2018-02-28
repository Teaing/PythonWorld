#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea
# 来自 《编写高质量代码-改善Python程序的91个建议》

import time
import Queue
import urllib2
import threading


def main():
    urls = ['http://www.ZZXX.com/', 'http://www.FFCC.com/', 'http://www.KKjj.com/']
    wm = WorkerManger(2)  # 创建线程池
    for i in urls:
        wm.add_job(download_file, i)
    wm.start()
    wm.wait_for_complete()


# 处理reuqest 的工作线程
class Worker(threading.Thread):
    def __init__(self, workQueue, resultQueue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue

    def run(self):
        while True:
            try:
                callable, args, kwds = self.workQueue.get(False)  # 从队列中取出一个任务
                res = callable(*args, **kwds)
                self.resultQueue.put(res)
            except Queue.Empty:
                break


# 线程池管理器
class WorkerManger:
    def __init__(self, num_of_workers=10):
        self.workQueue = Queue.Queue()  # 请求队列
        self.resultQueue = Queue.Queue()  # 输出结果的队列
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue)  # 创建工作线程
            self.workers.append(worker)  # 加入线程队列中

    def start(self):  # 启动线程
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()  # 从池中取出一个线程处理请求
            worker.join()

            if worker.is_alive() and not self.workQueue.empty():
                self.workers.append(worker)  # 重新加入线程池中
        print 'All jobs were completed.'

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))  # 往工作队列中加入请求

    def get_result(self, *args, **kwds):  # 获取处理结果
        return self.resultQueue.get(*args, **kwds)


def download_file(url):
    print 'begin download {0}'.format(url)
    urlHandler = urllib2.urlopen(url)
    fName = str(time.time()) + '.html'
    with open(fName, 'wb') as f:
        while True:
            chunk = urlHandler.read(1024)
            if not chunk:
                break
            f.write(chunk)


if __name__ == '__main__':
    main()
