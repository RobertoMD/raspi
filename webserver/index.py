#!/usr/bin/python
import os
import sys,socket
import time
import datetime
import shutil
import subprocess
import util
import RPi.GPIO as GPIO
import config
import radio
import bmp180 # just for status()
from flask import Flask,render_template,request,flash,session,redirect,url_for,g
from util import authenticate, check_auth, requires_auth

#Flask application
app=Flask(__name__)
app.config.from_object('config')
app.secret_key='mj)=89=Ji9mjI)Njij$$'

#GPIO INIT
#GPIO init on pin 11 (GPIO17)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
# First relay
GPIO.setup(config.LINES['R1LINE'],GPIO.OUT)
now=datetime.datetime.now().strftime(config.DATEFORMAT)

#----------------------------------------------------------------
@app.route("/")
@requires_auth
def index():
	now=datetime.datetime.now().strftime(config.DATEFORMAT)
	# cloud TS service status
	cloud='on' if util.isCloudActive() else 'off'
	# temperature
	fTemp1=util.getTemperature(0)
	temp1="%2.1f" % fTemp1
	# external temp
	r=radio.radio()	
	t=r.getTemp(2)
	text='N/A' if t is None else "%2.1f" % t
	# pressure
	p1=util.getPressure()
	# light
	s1=util.getLight(config.LINES['R1LINE'])
	# last time the ligth was switched off
	lastoff=util.db_getvalue(config.DB_LIGHTSOFF)
	if lastoff is None:
		loe='<no disponible>'
	else:
		loe=lastoff
	tData={
		'temp1':temp1,
		'text':text,
		'pres1':p1,
		's1':s1,
		'time':now,
		'loe':loe,
		'cloud':cloud
	}
	return render_template('index.html',**tData)

#----------------------------------------------------------------
@app.route("/s")
def status():
	tData={}
	ts=[]
	sw=[]
	pr=[]
	# internal temp
	for i,f in enumerate(config.TEMP_SENSORS):
		t=util.getTemperature(i)
		s='N/A' if t is None else "%2.1f" % t
		ts.append([f,config.TEMP_ALIAS[i],s])
	# external temp
	r=radio.radio()	
	t=r.getTemp(2)
	s='N/A' if t is None else "%2.1f" % t
	ts.append(['nrf24l01+','Exterior',s])
	for i in config.LINES.items():
		t=util.nvl(util.getLight(i[1]),'N/A')
		sw.append([i[0],i[1],t])
	p1=bmp180.BMP180()
	if p1._device._address:
		px="0x%x" % p1._device._address
	p2=util.nvl(util.getPressure(),'N/A')
	pr.append(['Presion',px,p2])
	tData={
		'ts':ts,
		'sw':sw,
		'pr':pr
	}
	return render_template('s.html',**tData)

#----------------------------------------------------------------
@app.route("/test")
def test():
	tData={}
	#fTemp1=util.getTemperature(0)
	#fTemp2=util.getTemperature(1)
	#fTemp3=util.getTemperature(2)
	# external temp
	#r=radio.radio()	
	#t=r.getTemp(2)
	#s='N/A' if t is None else "%2.1f" % t
	if request.remote_addr:
		tData={ 'remote':request.remote_addr,'agent':request.user_agent }
	return render_template('test.html',**tData)

#----------------------------------------------------------------
@app.route("/temp")
@requires_auth
def temp():
	tData={}
	ts=[]
	sw=[]
	pr=[]
	# internal temp
	for i,f in enumerate(config.TEMP_SENSORS):
		t=util.getTemperature(i)
		s='N/A' if t is None else "%2.1f" % t
		# [index, alias, value]
		ts.append([f,config.TEMP_ALIAS[i],s])
	# external temp
	r=radio.radio()	
	t=r.getTemp(2)
	s='N/A' if t is None else "%2.1f" % t
	ts.append([3,'Exterior',s])
	# relays
	for i in config.LINES.items():
		t=util.nvl(util.getLight(i[1]),'N/A')
		sw.append([i[0],i[1],t])
	# pressure
	p1=bmp180.BMP180()
	if p1._device._address:
		px="0x%x" % p1._device._address
	p2=util.nvl(util.getPressure(),'N/A')
	# [alias, address, pressure]
	pr.append(['Presion',px,p2])
	tData={
		'ts':ts,
		'sw':sw,
		'pr':pr,
	}
	return render_template('temp.html',**tData)

#----------------------------------------------------------------
@app.route("/conf", methods=['GET','POST'])
@requires_auth
def conf():
	cloud='on' if util.isCloudActive() else 'off'
	now=datetime.datetime.now().strftime(config.DATEFORMAT)
	res=None
	# if arrived here by submitting the form
	if request.method == 'POST':
		# get setting for webcam resolution
		res=request.form['res']
		util.db_setvalue(config.DB_WEBCAMRES,res)
		# get setting for cloud save desired state
		clds=request.form['cloud']
		# and try to start it if it was stopped
		if cloud=='off' and clds=='on':
			ps=subprocess.Popen("sudo /etc/init.d/thingspeak start", shell=True, stdout=subprocess.PIPE)
			flash('ThingSpeak daemon started')
		elif cloud=='on' and clds=='off':
			ps=subprocess.Popen("sudo /etc/init.d/thingspeak stop", shell=True, stdout=subprocess.PIPE)
			flash('ThingSpeak daemon stopped')
		flash('Settings saved')
	else:
		res=util.nvl(util.db_getvalue(config.DB_WEBCAMRES),'640x480')

	db=util.db_get()
	with db:
		c=db.cursor()
		q="SELECT * FROM ACCESS ORDER BY DATETIME DESC LIMIT 100"
		c.execute(q)
		rows=c.fetchall()
		log=''
		for row in rows:
			log=log+row[0]+';'+row[1]+';'+row[2]+';'+row[3]+';'+row[4]+'\n'
	tData={
		'cloud':cloud,
		'res':res,
		'time':now,
		'log':log
	}
	return render_template('conf.html',**tData)

#----------------------------------------------------------------
@app.route("/multi", methods=['GET','POST'])
@requires_auth
def multi():
	# if arrived here by submitting the form
	if request.method == 'POST':
		if "1d" in request.form:
			points="150"
		elif "3d" in request.form:
			points="450"
		elif "7d" in request.form:
			points="1010"
		else:
			points="450"
	else:
		points="450"
	tData={
		'points':points
	}
	return render_template('multi.html',**tData)

#----------------------------------------------------------------
@app.route("/light", methods=['GET','POST'])
@requires_auth
def light():
	now=datetime.datetime.now()
	lastoff=util.db_getvalue(config.DB_LIGHTSOFF)
	if lastoff is None:
		flash('No Last Lights Out Event.')
		lastoff=now.strftime(config.DBDATEFORMAT)
	# if arrived here by submitting the form, perform the action
	if request.method == 'POST':
		value=request.form['value']
		line=request.form['line'] 
		if line not in config.LINES.keys() or value not in {'on','off'}:
			flash('Internal error. No lights changed.')
			return redirect(url_for('/'))
		s=True if value=='on' else False
		if "Apagar15" in request.form:
			cpid=os.fork()
			if cpid==0:
				time.sleep(15)
				util.setLight(config.LINES[line],s)
				shutdown=request.environ.get('werkzeug.server.shutdown')
				shutdown()
		elif "Apagar60" in request.form:
			cpid=os.fork()
			if cpid==0:
				time.sleep(60)
				util.setLight(config.LINES[line],s)
				shutdown=request.environ.get('werkzeug.server.shutdown')
				shutdown()
		else:
			util.setLight(config.LINES[line],s)
		# write switch off event to db
		if not s:
			util.db_setvalue(config.DB_LIGHTSOFF,now.strftime(config.DBDATEFORMAT))
			lastoff=None
	s1=util.getLight(config.LINES['R1LINE'])
	if lastoff is None:
		delta=None
	else:
		delta=now-datetime.datetime.strptime(lastoff,'%Y-%m-%d %H:%M:%S')
	tData={
		's1':s1,
		'time':now.strftime(config.DATEFORMAT),
		'lastoff':util.prettydelta(delta)
	}
	return render_template('light.html',**tData)

#----------------------------------------------------------------
@app.route("/picdb",methods=['GET','POST'])
@requires_auth
def picdb():
	# if arrived here by submitting the form in itself
	if request.method == 'POST':
		action=request.form['action']
		if action not in {'delete'}:
			flash('Internal error. Wrong form action.')
			return redirect(url_for('/picdb'))
		if action=='delete':
			file=request.form['file']
			os.remove(os.getcwd()+'/static/img/h/'+file)
			flash('Imagen '+file+' borrada.')
	# if arrived here directly
	now=datetime.datetime.now().strftime(config.DATEFORMAT)
	# get file list
	files=os.listdir(os.getcwd()+'/static/img/h')
	tData={
		'time':now,
		'files':files
	}
	return render_template('picdb.html',**tData)
	
#----------------------------------------------------------------
@app.route("/pic",methods=['GET','POST'])
@requires_auth
def pic():
	# if arrived here by submitting the form in itself
	if request.method == 'POST':
		if request.form.has_key('update'):
			util.takePicture()
		elif request.form.has_key('save'):
			src=os.getcwd()+'/static/img/still.jpg'
			dst=os.getcwd()+'/static/img/h/still'+str(int(os.stat('index.py').st_ctime))+'.jpg'
			shutil.copy(src,dst)
			flash('Imagen guardada.')
		else:
			flash('Desastrosus error.')
			return redirect(url_for('/pic'))
	# if arrived here directly
	else:
		util.takePicture()
	now=datetime.datetime.now().strftime(config.DATEFORMAT)
	tData={ 'time':now }
	return render_template('pic.html',**tData)

#----------------------------------------------------------------
@app.before_request
def before_request():
	if not request.path.startswith('/static'):
		now=datetime.datetime.now().strftime(config.DBDATEFORMAT)
		try:
			a=request.remote_addr
		except:
			a='Unknown'
		try:
			host=str(socket.gethostbyaddr(request.remote_addr)[0])
		except:
			host='Unknown'
		db=util.db_get()
		with db:
			c=db.cursor()
			q="INSERT INTO ACCESS VALUES (?,?,?,?,?)"
			r=request.method+' '+request.path
			c.execute(q,(now,a,host,r,repr(request.user_agent)))
		return

#----------------------------------------------------------------
if __name__=="__main__":
	app.run(host='0.0.0.0',port=80,debug=True)
