#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
LABEL_TEMP1 = u'Salón'
LABEL_TEMP2 = u'Salón2'
# Lines (relays) list
LINES={'R1LINE':11}
# Line for first relay
LINENAMES={'R1LINE':u'del salón'}
#temperature sensors
DEVPATH='/sys/bus/w1/devices/'
TEMP_SENSORS=['28-000003c63391','28-000003be20b5']
TEMP_ALIAS=[u'Salón 1',u'Salón 2']
#Database
DATABASE=os.getcwd()+'/casatron.db'
USERNAME='admin'
PASSWORD='nimda'
SECRET_KEY='mj)=89=Ji9mjI)Njij$$'
#misc
DATEFORMAT='%d %b %H:%M'
DBDATEFORMAT='%Y-%m-%d %H:%M:%S'
DB_LIGHTSOFF='lights.off.timestamp'
DB_WEBCAMRES='webcam.resolution'
