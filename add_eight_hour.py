def add_eight_hour(time_str):
	return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(hours=int(8))
	#return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')) + 28800)))
  
  
  time_str = '2016-11-30 17:08:31.502916'
