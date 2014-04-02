#!/usr/bin/env python
import cgi
form=cgi.FieldStorage()
print "Content-type: text/html"
"""
<html>
<title>main page</title>
"""
cgi.test()
print "hola tron"
print form
"""
</html>
"""

