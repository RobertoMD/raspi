#!/usr/bin/python
import httplib, urllib
import datetime
import time
import os
import util
 
def sendData():
	try:
		temp1=util.getTemperature(0)
		temp2=util.getTemperature(1)
		pressure=util.getPressure()
		params = urllib.urlencode({'field1': temp1, 'field2': temp2, 'field3': pressure, 'key':'M3WA24ZHF4KDYM56'})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("api.thingspeak.com:80")
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print response.status, response.reason
		data = response.read()
		conn.close()
	except Exception:
		pass
 
#sleep for 300 seconds (api limit of 15 secs)
if __name__ == "__main__":
	# start checks - print data at startup
	temp1=util.getTemperature(0)
	temp2=util.getTemperature(1)
	pressure=util.getPressure()
	params = urllib.urlencode({'field1': temp1, 'field2': temp2, 'field3': pressure, 'key':'M3WA24ZHF4KDYM56'})
	print temp1," degrees"
	print temp2," degrees"
	print pressure, " mbar"
	print params
	# end checks
	now=datetime.datetime.now()
	d=datetime.datetime(now.year,now.month,now.day,now.hour,0,0)
	delta=(now-d).total_seconds()
	print "delta es ",d
	r=int(delta)/600*600+600-int(delta)
	print "Waiting",r,"seconds for synchronization"
	time.sleep(r)
	while True:
		sendData()
		time.sleep(600)
