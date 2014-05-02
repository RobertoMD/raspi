#!/usr/bin/python
import os
import sys
import time
import datetime
import util
import subprocess
from flask import Flask,render_template
from util import authenticate, check_auth, requires_auth

app=Flask(__name__)
now=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
@app.route("/")
@requires_auth
def index():
	tData={ 'time':now }
	return render_template('index.html',**tData)

@app.route("/main")
@requires_auth
def main():
	fTemp1=util.getTemperature(0)
	fTemp2=util.getTemperature(1)
	if fTemp1 is None or fTemp2 is None:
		return render_template('no-w1.html')
	else:
		#now=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
		temp1="%2.1f" % fTemp1
		temp2="%2.1f" % fTemp2
		tData={
			'temp1':temp1,
			'temp2':temp2,
			'time':now
		}
		return render_template('main.html',**tData)

@app.route("/conf")
@requires_auth
def conf():
	s1='off' # cloud service active
	ps=subprocess.Popen("ps -ef | grep '/usr/bin/python /home/pi/cloud/ts.py' | grep -v grep | wc -l", shell=True, stdout=subprocess.PIPE)	
	res=ps.stdout.readline().rstrip()
	if res == '1':
		s1='on'
	#now=datetime.datetime.now().strftime('%d %b %H:%M')
	tData={
		's1':s1,
		'time':now
	}
	return render_template('conf.html',**tData)

@app.route("/multi")
@requires_auth
def multi():
	return render_template('multi.html')
if __name__=="__main__":
	app.run(host='0.0.0.0',port=80,debug=True)
