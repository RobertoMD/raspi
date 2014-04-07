#!/usr/bin/python
import cgi
import cgitb
import os
import glob
import time
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
cgitb.enable()
DEVFILE='/sys/bus/w1/devices/28-000003c63391/w1_slave'
def read18B20():
	f=open(DEVFILE,'r')
	lines=f.readlines()
	f.close()
	return lines
lines=read18B20()
while lines[0].strip()[-3:] != 'YES':
	time.sleep(0.2)
	lines=read18B20()
f=float(lines[1].split('=')[1])/1000.
temp="%2.1f" % f
form=cgi.FieldStorage()
html="""Content-type: text/html\r\n\r\n
<html>
<title>main page</title>
<link rel="stylesheet" type="text/css" href="../s.css" />
<body>
<h1>Temp: TAG_TEMP &deg;C</h1>
</body>
</html>"""
html=html.replace("TAG_TEMP",temp)
print html
#cgi.test()
#print form
#print "<br>\n"
#print form.keys()
#print "<br>\n"
#print form.getvalue('pin')
#print "<br>\n"
