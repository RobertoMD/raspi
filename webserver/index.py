#!/usr/bin/python
import os
import sys
import time
import datetime
import shutil
import subprocess
import util
import RPi.GPIO as GPIO
import config
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
		's1':s1,
		'time':now,
		'loe':loe,
		'cloud':cloud
	}
	return render_template('index.html',**tData)

#----------------------------------------------------------------
@app.route("/test")
def test():
	return render_template('test.html')

#----------------------------------------------------------------
@app.route("/temp")
@requires_auth
def temp():
	fTemp1=util.getTemperature(0)
	fTemp2=util.getTemperature(1)
	if fTemp1 is None or fTemp2 is None:
		return render_template('no-w1.html')
	else:
		now=datetime.datetime.now().strftime(config.DATEFORMAT)
		temp1="%2.1f" % fTemp1
		temp2="%2.1f" % fTemp2
		tData={
			'temp1':temp1,
			'temp2':temp2,
			'time':now
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
	tData={
		'cloud':cloud,
		'res':res,
		'time':now
	}
	return render_template('conf.html',**tData)

#----------------------------------------------------------------
@app.route("/multi")
@requires_auth
def multi():
	return render_template('multi.html')


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
if __name__=="__main__":
	app.run(host='0.0.0.0',port=80,debug=True)

