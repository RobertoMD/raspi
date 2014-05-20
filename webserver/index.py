#!/usr/bin/python
import os
import sys
import time
import datetime
import shutil
import util
import RPi.GPIO as GPIO
from flask import Flask,render_template,request,flash,session,redirect,url_for
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
GPIO.setup(app.config['LINES']['R1LINE'],GPIO.OUT)
now=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

#----------------------------------------------------------------
@app.route("/")
@requires_auth
def index():
	# temperature
	fTemp1=util.getTemperature(0)
	temp1="%2.1f" % fTemp1
	# light
	s1=util.getLight(app.config['LINES']['R1LINE'])
	tData={
		'temp1':temp1,
		's1':s1,
		'time':now 
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
		now=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
		temp1="%2.1f" % fTemp1
		temp2="%2.1f" % fTemp2
		tData={
			'temp1':temp1,
			'temp2':temp2,
			'time':now
		}
		return render_template('temp.html',**tData)

#----------------------------------------------------------------
@app.route("/conf")
@requires_auth
def conf():
	s1='on' if util.isCloudActive() else 'off'
	now=datetime.datetime.now().strftime('%d %b %H:%M')
	tData={
		's1':s1,
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
	# if arrived here by submitting the form
	if request.method == 'POST':
		value=request.form['value']
		line=request.form['line'] 
		if line not in app.config['LINES'].keys() or value not in {'on','off'}:
			flash('Internal error. No lights changed.')
			return redirect(url_for('/'))
		#s=util.getLight(app.config['LINES']['R1LINE])
		s=True if value=='on' else False
		util.setLight(app.config['LINES'][line],s)
	s1=util.getLight(app.config['LINES']['R1LINE'])
	now=datetime.datetime.now().strftime('%d %b %H:%M')
	tData={
		's1':s1,
		'time':now
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
	now=datetime.datetime.now().strftime('%d %b %H:%M')
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
		action=request.form['action']
		if action not in {'pic','save'}:
			flash('Internal error. Wrong form action.')
			return redirect(url_for('/'))
		if action=='pic':
			util.takePicture()
		elif action=='save':
			src=os.getcwd()+'/static/img/still.jpg'
			dst=os.getcwd()+'/static/img/h/still'+str(int(os.stat('index.py').st_ctime))+'.jpg'
			shutil.copy(src,dst)
			flash('Image saved.')
	# if arrived here directly
	else:
		util.takePicture()
	now=datetime.datetime.now().strftime('%d %b %H:%M')
	tData={ 'time':now }
	return render_template('pic.html',**tData)

#----------------------------------------------------------------
if __name__=="__main__":
	app.run(host='0.0.0.0',port=80,debug=True)
