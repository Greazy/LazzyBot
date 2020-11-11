import sqlite3 as sql
from threading import Thread

con = sql.connect('our.db')
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM 'chat_id'")
    rows = cur.fetchall()
    for row in rows:
    	print(row[0])

    con.commit()

