#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import Queue
import threading


def main():
	thread_num = 50
	queue = Queue.Queue()
	for i in range(thread_num):
		t = Print_Threading(queue)
		t.setDaemon(True)
		t.start()

	for n in xrange(100):
		queue.put(n)

	queue.join()


class Print_Threading(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			result = self.queue.get()
			if mutex.acquire():
				if result:
					print self.Action(result)
			mutex.release()
			self.queue.task_done()

	def Action(self, result_str):
		if result_str:
			return result_str.__str__()

mutex = threading.Lock()

if __name__ == '__main__':
	main()
