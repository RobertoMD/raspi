#!/usr/bin/python
import traceback
import sys
import sqlite3 as s
db=s.connect('../casatron.db')
db.row_factory=s.Row
out=False
savesql=''
while not out:
	sql=raw_input('sql> ')
	if sql != 'exit':
		if sql.lower() == 'r':
			sql=savesql
		if sql != '':
			cur=db.cursor()
			try:
				cur.execute(sql)
				db.commit()
				rows=cur.fetchall()
				for row in rows:
					print row
				if len(rows) >0:
					print str(len(rows))+" rows"
				else:
					print 'Ok'
				savesql=sql
			except s.Error, e:
				#traceback.print_exc(limit=1,file=sys.stdout)
				sys.stdout.write("\033[31m")
				print e
				sys.stdout.write("\033[0m")
				if db:
					db.rollback()
			except EOFError, e:
				if db:
					db.rollback()
					out=True
	else:
		out=True
db.close()
	
