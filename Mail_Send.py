#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:Tea

import smtplib
from email.mime.text import MIMEText

class Mail_Send:
	_mail_to_list= ['admin@abc.com']
	_mail_host = 'smtp.abc.com'
	_mail_username = 'admin'
	_mail_password = 'admin123'
	_mail_postfix = 'abc.com'

	@staticmethod
	def send(sub, content):
		_me = "admin<" + Mail_Send._mail_username + "@" + Mail_Send._mail_postfix + ">"
		_msg = MIMEText(content, _subtype='plain', _charset='utf-8')
		_msg['Subject'] = sub
		_msg['From'] = _me
		_msg['To'] = ";".join(Mail_Send._mail_to_list)
		try:
			server = smtplib.SMTP()
			server.connect(Mail_Send._mail_host)
			server.login(Mail_Send._mail_username, Mail_Send._mail_password)
			server.sendmail(_me, Mail_Send._mail_to_list, _msg.as_string())
			server.close()
		except Exception,e:
			print e
