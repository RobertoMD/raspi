import os
import time
import bmp180
from functools import wraps

#read DS18B20device
DEVPATH='/sys/bus/w1/devices/'
DEVICES=['28-000003c63391','28-000003be20b5','28-000003be1727']

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
#temp read loop

def getTemperature(sensor):
	file=DEVPATH+DEVICES[sensor]+'/w1_slave'
	lines=getContent(file)
	if lines is None:
		return None
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.4)
		lines=getContent(file)
		if lines is None:
			return None
	return float(lines[1].split('=')[1])/1000.

#BMP180 Pressure read
def getPressure():
	sensor=bmp180.BMP180()
	mb=sensor.read_pressure()/100
	return mb


