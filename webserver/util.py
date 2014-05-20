#!/usr/bin/python
import os
import time
import subprocess
import RPi.GPIO as GPIO
from functools import wraps
from flask import request, Response

DEVPATH='/sys/bus/w1/devices/'
DEVICES=['28-000003c63391','28-000003be20b5']
R1LINE=11

######################
def getContent(file):
	if not os.path.exists(file):
		return None
	try:
        	f=open(file,'r')
        	lines=f.readlines()
        	f.close()
	except:
		return None
	return lines
#temp read loop

######################
def getTemperature(sensor):
	file=DEVPATH+DEVICES[sensor]+'/w1_slave'
	lines=getContent(file)
	if lines is None:
		return None
	while lines[0].strip()[-3:] != 'YES':
        	time.sleep(0.4)
		lines=getContent(file)
		if lines is None:
			return None
	return float(lines[1].split('=')[1])/1000.

######################
def getLight(line):
	cs=GPIO.input(line)
	return 'on' if cs else 'off'

######################
def setLight(line,value):
	GPIO.output(line,value)
	return

######################
def takePicture():
	ps=subprocess.Popen('fswebcam -r 352x288 '+os.getcwd()+'/static/img/still.jpg', shell=True, stdout=subprocess.PIPE)
	return

######################
def isCloudActive():
	ps=subprocess.Popen("ps -ef | grep '/usr/bin/python /home/pi/cloud/ts.py' | grep -v grep | wc -l", shell=True, stdout=subprocess.PIPE)
	res=ps.stdout.readline().rstrip()
	if res == '1':
		return True
	return False

#AUTH functions
######################
def check_auth(username,password):
	if username=='guest' and password=='8022':
		return True
	return password=='1196' 

######################
def authenticate():
	return Response('Sin acceso.\nConectate comme il faut',401,{'WWW-Authenticate': 'Basic realm="Se requiere clave"'})

######################
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated
