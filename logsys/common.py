import pdb
import uuid
import os
import datetime

from django.conf import settings

class Log(object):

	def	open_log_file(self, app_type, app_id, prefix):
		if app_id == '-1':
		   filename = str((prefix+'_'+str(uuid.uuid4()).replace('-','_')  + '.txt'))
		else:
		   filename = str(app_id) + '.txt'
		  
		if app_type == '0':   
			dir = os.path.join(settings.LOG_FILE_DIR, 'fix')
			if not os.path.isdir(dir):
				os.makedirs(dir)
		else:
			dir = os.path.join(settings.LOG_FILE_DIR, 'problem')
			if not os.path.isdir(dir):
				os.makedirs(dir)

		filename = os.path.join(dir, filename)
		if os.path.isfile(filename):
			file = open(filename, 'a')
			return file
		else:
			file = open(filename, 'w')
			return file
		
	def	write(self, filename, operatorname, msg):
		msg = ('\n[%s] ---- [%s] ---- %s'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'), operatorname, msg))
		filename.write(msg)
		filename.flush()

	def	close_log_file(self, filename):
		filename.close()
		
	def	renamefile(self, filesrc, filedst, app_type):
		try:
			if app_type == '0':
				os.rename(filesrc.name,os.path.join(settings.LOG_FILE_DIR, 'fix', (str(filedst)+'.txt')))
			else:
				os.rename(filesrc.name,os.path.join(settings.LOG_FILE_DIR, 'problem', (str(filedst)+'.txt')))
				
		except OSError as e:
			return e
