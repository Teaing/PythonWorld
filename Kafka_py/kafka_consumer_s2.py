#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:Tea

from kafka import KafkaConsumer

def main():
	consumer = KafkaConsumer('fuckyou',
                         group_id=None,
                         bootstrap_servers=['192.168.111:9092','192.168.112:9092','192.168.113:9092','192.168.114:9092','192.168.115:9092'])
	for message in consumer:
		print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
	                                      message.offset, message.key,
	                                      message.value))
if __name__ == '__main__':
	main()
