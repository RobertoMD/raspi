#!/usr/bin/python
webdir='./www'
port=80
import os,sys
from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
os.chdir(webdir)
srvaddr=("",80)
srvobj=HTTPServer(srvaddr,CGIHTTPRequestHandler)
srvobj.serve_forever()
