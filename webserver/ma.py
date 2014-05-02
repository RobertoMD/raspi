#!/usr/bin/python
import cgi
import cgitb
import os,sys
import glob
import time
import util
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
cgitb.enable()
DEVFILE='/sys/bus/w1/devices/28-000003c63391/w1_slave'

#html header
htmlHeader="""Content-type: text/html\r\n\r\n
<html>
<title>Los Jubetes</title>
<link rel="stylesheet" type="text/css" href="/s.css" />
<body>
"""

#html body
htmlBody="""
<h1>Temp: TAG_TEMP &deg;C</h1>
"""

#html footer
htmlFooter="""
</body>
</html>
"""

#read device
def read18B20():
	f=open(DEVFILE,'r')
	lines=f.readlines()
	f.close()
	return lines

#get Pin
if not util.pinOk():
	print htmlHeader+"<a href='/'><H1>PIN is chung</H1></a>"+htmlFooter
	sys.exit()

#temp read loop
lines=read18B20()
while lines[0].strip()[-3:] != 'YES':
	time.sleep(0.2)
	lines=read18B20()
f=float(lines[1].split('=')[1])/1000.
temp="%2.1f" % f

print htmlHeader+htmlBody.replace("TAG_TEMP",temp)+htmlFooter

