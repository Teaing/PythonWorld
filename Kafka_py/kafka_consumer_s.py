#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:Tea

import json
import pykafka

def main():
	kafka_client = pykafka.KafkaClient(hosts='192.168.1.11:9092,192.168.1.12:9092,192.168.1.13:9092,192.168.1.14:9092,192.168.1.15:9092',socket_timeout_ms=3000)
	print kafka_client.topics
	topic = kafka_client.topics['login_info']
	consumer = topic.get_simple_consumer()
	for message in consumer:
		if message is not None:
			print message.offset
			print json.loads(message.value)['ip']

if __name__ == '__main__':
	main()
