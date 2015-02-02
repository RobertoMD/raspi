#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from nrf24 import NRF24
import time,random,string

#GPIO.cleanup()

#------------------------------------------------
class radio(NRF24):
	radio=None
	pipe_r=0xc2e6e6e6e6
	pipe_w=0xe7e7e7e7e7
	CMD_PING='P'
	CMD_TEMP='T'
	CMD_RANDOM='R'
	CMD_VERBOSE='V'
	CMD_CHANNEL='C'

	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		self.radio = NRF24()
		self.radio.begin(0, 0, 12)
		self.radio.setRetries(15,15)
		self.radio.setPayloadSize(32)
		self.radio.setChannel(0x18)
		self.radio.enableDynamicPayloads()
#		self.radio.enableAckPayload()
		self.radio.setAutoAck(True)
		self.radio.setDataRate(NRF24.BR_1MBPS)
#		self.radio.setDataRate(NRF24.BR_250KBPS)
		self.radio.setPALevel(NRF24.PA_MAX)

		self.radio.openWritingPipe(self.pipe_w)
		self.radio.openReadingPipe(1, self.pipe_r)
		# enter standby mode (?)
		self.radio.startListening()
		self.radio.stopListening()
		# print config
		self.radio.printDetails()

#------------------------------------------------
	def printDetails(self):
		self.radio.printDetails()
#------------------------------------------------
	def send(self,msg):
		self.radio.stopListening()
		r=self.radio.write(msg);
		self.radio.startListening()
		return r;
#------------------------------------------------
	def recv(self):
		b=[]
		if self.radio.available():
			ps=self.radio.getDynamicPayloadSize()
			self.radio.read(b,ps)
			s=string.join(map(unichr,b),'')
			return s
		else:
			return None
#------------------------------------------------
	def getTemp(self):
		rc=None
		if (self.send('T') == 32):
			time.sleep(2)
			rc=self.recv()
			if rc is not None:
				rc=float(rc.split(';')[3])
		return rc
