#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea


import threading
import Queue


def main():
    inputQueue = Queue.Queue()  # 输入队列
    outputQueue = Queue.Queue()  # 输出队列,获取计算后结果
    inputDataList = list(range(2001))  # 源数据
    outputDataList = []  # 结果集

    threadNum = 10

    for i in range(threadNum):
        t = MyThreading(inputQueue, outputQueue)
        t.setDaemon(True)
        t.start()

    for line in inputDataList:
        inputQueue.put(line)

    inputQueue.join()

    while not outputQueue.empty():
        outputDataList.append(outputQueue.get())
        outputQueue.task_done()

    # outputQueue.join()

    print outputDataList


class MyThreading(threading.Thread):
    def __init__(self, inputQueue, outputQueue):
        threading.Thread.__init__(self)
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue

    def run(self):
        while True:
            numberData = self.inputQueue.get()
            self.value = self.addNumber(numberData)
            self.outputQueue.put(self.value)
            self.inputQueue.task_done()

    def addNumber(self, numberData):
        return pow(numberData, 2)


if __name__ == '__main__':
    main()
