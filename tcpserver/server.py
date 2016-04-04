#!/usr/bin/python
 
import socket
import time
 
# Accept requests from any IP address on port 50000
TCP_IP = '0.0.0.0'
TCP_PORT = 5000
BUFFER_SIZE = 4096
 
# Create socket and bind it to TCP address &amp; port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
 
t=None
v=None
# Infinite loop
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
# Listen for a connection
s.listen(10)
while 1:
	try:
		print "..."
		# Connection found. Accept connection
		conn, addr = s.accept()
		print ("%s:" % addr[0])
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print data
		if data.startswith('T:'):
			#f=float(data.split(':')[1])
			t=data;
		elif data.startswith('V:'):
			#v=float(data.split(':')[1])
			v=data;
		elif data=='GET':
			if t is None:
				print "enviando none"
				s.sendall('T:None')
			else:
				print "enviando t"
				s.sendall(t)
			if v is None:
				print "enviando nonev"
				s.sendall('V:None')
			else:
				print "enviando v"
				s.sendall(v)
		else:
			continue
		print "cerrando"
		s.shutdown()
		s.close()
	except socket.error,msg:
		print 'Socket error '+str(msg[0])+': '+str(msg[1])+'.Retrying in 10 seconds'
		time.sleep(10);

