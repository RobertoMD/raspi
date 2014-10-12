import sqlite3
db=sqlite3.connect('../casatron.db')
f=open('casatron.sql','r')
db.cursor().executescript(f.read())
db.commit()
db.close()
