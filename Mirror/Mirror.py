#!/usr/bin/env python
# -*- coding: utf_8 -*-
# author: Tea

import sys
import time
import platform
import subprocess


def main():
	system_version = Get_System_Version()
	Sleep_Time = App_Info()['interval_time']
	while True:
		Action_Start(system_version)
		Active_Sleep(Sleep_Time)


def Action_Start(_system_ver):
	process_list = App_Info()['process']
	print 'Mirror Process Count: %d ' % process_list.__len__()
	if _system_ver == 'windows':
		# mirror_code = ''.join(['TASKLIST.exe /V /NH /FO csv /FI "IMAGENAME eq ',process_name,'"'])  # pass
		try:
			p = subprocess.Popen(['TASKLIST.exe', '/V', '/NH', '/FO', 'CSV', '/FI', 'STATUS eq running'], bufsize=0,
			                     stdout=subprocess.PIPE)
		except Exception, e:
			pass
		mirror_output = p.communicate()[0]
		mirror_process_list = mirror_output.split('\r\n')
		if mirror_process_list:
			for _process in process_list:
				Action_tag = False
				for process_one_list in mirror_process_list:
					process_one = process_one_list.split(',')
					process_name = process_one[0][1:-1]  # Process Name, Replace ""
					process_des = process_one[-1]  # Process Describe use e.g: python.exe hello.py
					if _process == process_name:
						Action_tag = True
						break
					elif _process in process_des:
						Action_tag = True
						break
				Check_Tag_Send_Message(_process, Action_tag)
	elif _system_ver == 'linux':
		for _process in process_list:
			Action_tag = False
			try:
				process_exec = subprocess.Popen('ps -ef|grep ' + _process + '|grep -v \'grep ' + _process + '\'',
				                                shell=True, bufsize=0,
				                                stdout=subprocess.PIPE)
			except Exception, e:
				pass
			mirror_output = process_exec.communicate()[0]
			if mirror_output:
				Action_tag = True
			Check_Tag_Send_Message(_process, Action_tag)
	else:
		sys.exit('What The Fuck...')


	# Check Found Tag
def Check_Tag_Send_Message(process_name, action_tag):
	check_tag = App_Info()['check_live_status']
	if check_tag:
		if action_tag:
			Send_Warning_Message(process_name)
		else:
			Send_Warning_Message(process_name, False)
	else:
		if action_tag is False:
			Send_Warning_Message(process_name, False)
			sys.exit('Game Over')


	# Get System Type
def Get_System_Version():
	if 'Windows' in platform.system():
		system_ver = 'windows'
	elif 'Linux' in platform.system():
		system_ver = 'linux'
	else:
		system_ver = 'other'
	print 'System Version: %s' % system_ver
	return system_ver


	# Send warning message
def Send_Warning_Message(process_name, action_tag=True):  # action_tag True is running ,False is Die
	now_str = Get_Now()
	if action_tag:
		message = ''.join(['Process: ', process_name, ' is Active', '\n', 'Time: ', now_str])
	else:
		message = ''.join(['Process: ', process_name, ' is die', '\n', 'Time: ', now_str])
	print message
	# Send message Code ...


	# Get Now Time
def Get_Now():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))


	# Sleep Time
def Active_Sleep(time_int):
	sleep_sec = time_int * 60
	time.sleep(sleep_sec)

	# Return Config
def App_Info():
	app_info = dict(
		process=['main.py', 'action_post.exe'],  # Process Name
		mobile=['13666666666'], # Mobile Number use Send_Warning_Message
		email=['king@king.com'],    # Email Address use Send_Warning_Message
		interval_time=10,  # /min
		check_live_status=True  # False Is Die Send Message, True Is Send Message Every Action
	)
	return app_info


if __name__ == '__main__':
	main()
