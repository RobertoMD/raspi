#!/usr/bin/python
import httplib, urllib
import time
import os
import util
 
def doit():
	temp1=util.getTemperature(0)
	temp2=util.getTemperature(1)
	params = urllib.urlencode({'field1': temp1, 'field2': temp2, 'key':'M3WA24ZHF4KDYM56'})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com:80")
	conn.request("POST", "/update", params, headers)
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	conn.close()
 
#sleep for 300 seconds (api limit of 15 secs)
if __name__ == "__main__":
    while True:
        doit()
        time.sleep(600)
