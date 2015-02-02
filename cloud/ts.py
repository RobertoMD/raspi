#!/usr/bin/python
import httplib, urllib
import datetime
import time
import os
import util
import radio
 
def sendData(radio):
	try:
		temp1=util.getTemperature(0)
		temp2=util.getTemperature(1)
		temp3=util.getTemperature(2)
		pressure=util.getPressure()
		temp4=radio.getTemp()
		if temp4 is None:
			params = urllib.urlencode({'field1': temp1, 'field2': temp2, 'field3': pressure, 'field4': temp3, 'key':'M3WA24ZHF4KDYM56'})
		else:
			params = urllib.urlencode({'field1': temp1, 'field2': temp2, 'field3': pressure, 'field4': temp3, 'field5': temp4, 'key':'M3WA24ZHF4KDYM56'})
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
	radio=radio.radio()
	temp1=util.getTemperature(0)
	temp2=util.getTemperature(1)
	temp3=util.getTemperature(2)
	pressure=util.getPressure()
	temp4=radio.getTemp()
	print temp1," degrees"
	print temp2," degrees"
	print temp3," degrees"
	print pressure, " mbar"
	if radio is None:
		params = urllib.urlencode({'field1': temp1, 'field2': temp2, 'field3': pressure, 'field4': temp3, 'key':'M3WA24ZHF4KDYM56'})
	else:
		params = urllib.urlencode({'field1': temp1, 'field2': temp2, 'field3': pressure, 'field4': temp3, 'field5': temp4, 'key':'M3WA24ZHF4KDYM56'})
		print temp4," degrees"
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
		sendData(radio)
		time.sleep(600)
