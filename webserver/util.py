#!/usr/bin/python
import os
import time,datetime
import subprocess
import RPi.GPIO as GPIO
import config
import sqlite3
from functools import wraps
from flask import request,Response,g

#----------------------------------------------------------------
# MISC
#----------------------------------------------------------------

#----------------------------------------------------------------
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

#----------------------------------------------------------------
def prettydelta(delta):
	if delta is None:
		return 'un instante'
	r=''
	d=delta.days
	h=delta.seconds/3600
	m=(delta.seconds-h*3600)/60
	s=delta.seconds-h*3600-m*60
	if d>0:
		r="%d dias," % d
	if h>0 or (h==0 and r!=''):
		r=r+("%d horas " % h)
	if m>0 or (m==0 and r!=''):
		r=r+("%d minutos " % m)
	r=r+("%d segundos" %s)
	return r

#----------------------------------------------------------------
# Sensors, cameras
#----------------------------------------------------------------

#----------------------------------------------------------------
def getTemperature(sensor):
	file=config.DEVPATH+config.TEMP_SENSORS[sensor]+'/w1_slave'
	lines=getContent(file)
	if lines is None:
		return None
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.4)
		lines=getContent(file)
		if lines is None:
			return None
	return float(lines[1].split('=')[1])/1000.

#----------------------------------------------------------------
def getLight(line):
	cs=GPIO.input(line)
	return 'on' if cs else 'off'

#----------------------------------------------------------------
def setLight(line,value):
	GPIO.output(line,value)
	return

#----------------------------------------------------------------
def takePicture():
	res=nvl(db_getvalue(config.DB_WEBCAMRES),'640x480')
	ps=subprocess.Popen('fswebcam -r '+res+' '+os.getcwd()+'/static/img/still.jpg', shell=True, stdout=subprocess.PIPE)
	return

#----------------------------------------------------------------
def isCloudActive():
	ps=subprocess.Popen("ps -ef | grep '/usr/bin/python /home/pi/cloud/ts.py' | grep -v grep | wc -l", shell=True, stdout=subprocess.PIPE)
	res=ps.stdout.readline().rstrip()
	if res == '1':
		return True
	return False

#----------------------------------------------------------------
# AUTH
#----------------------------------------------------------------
def check_auth(username,password):
	if username=='guest' and password=='8022':
		return True
	return password=='1196' 

#----------------------------------------------------------------
def authenticate():
	return Response('Sin acceso.\nConectate comme il faut',401,{'WWW-Authenticate': 'Basic realm="Se requiere clave"'})

#----------------------------------------------------------------
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

#----------------------------------------------------------------
#DATABASE
#----------------------------------------------------------------
#Database connect
def db_connect():
	db=sqlite3.connect(config.DATABASE)
	db.row_factory=sqlite3.Row
	return db
#----------------------------------------------------------------
#Database init
def db_get():
	if not hasattr(g,'sqlite_db'):
		g.sqlite_db=db_connect()
	return g.sqlite_db

#----------------------------------------------------------------
#@app.teardown_appcontext
def db_close():
	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()
#----------------------------------------------------------------
def db_getvalue(p):
	db=db_get()
	with db:
		c=db.cursor()
		q="SELECT VALUE FROM CONFIG WHERE NAME like '"+p+"'"
		c.execute(q)
		row=c.fetchone()
		if row is None:
			return None
		return row[0]
#----------------------------------------------------------------
def db_setvalue(p,v):
	db=db_get()
	with db:
		c=db.cursor()
		c.execute("REPLACE INTO CONFIG(NAME,VALUE) VALUES('"+p+"','"+v+"')")
#----------------------------------------------------------------
def nvl(a,b):
	if a is None:
		return b
	return a

