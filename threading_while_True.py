#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import time
import Queue
import threading

def main():
	threading_num = 10
	queue = Queue.Queue()
	Forum_List = ['a', 'A', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'f', 'F','g','G','H','h','i','I']
	for num in range(threading_num):
		t = Threading_Print(queue)
		t.setDaemon(True)
		t.start()

	while True:
		for fid in Forum_List:
			queue.put(fid)

		queue.join()
		time.sleep(5)


class Threading_Print(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			print 'Threading Count: %d ' % threading.active_count()
			fid = self.queue.get()
			print 'Result: %s ' % fid
			self.queue.task_done()


if __name__ == '__main__':
	main()
