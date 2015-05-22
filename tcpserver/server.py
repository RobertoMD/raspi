#!/usr/bin/python
 
import socket
from subprocess import call
 
# Accept requests from any IP address on port 50000
TCP_IP = '0.0.0.0'
TCP_PORT = 79
BUFFER_SIZE = 4096
 
# Create socket and bind it to TCP address &amp; port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
 
# Infinite loop
while 1:
	# Listen for a connection
	s.listen(10)
	print "Awaiting connections"
	# Connection found. Accept connection
	conn, addr = s.accept()
	print ("Listening data from %s" % addr[0])
	while 1:
		print "connected: waiting for data"
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print data
		if data=='EXIT': break
	conn.close()
