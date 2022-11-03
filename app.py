import globalss as gb
import loginAPI
import messageAPI
import apsw
from apsw import Error
from globalss import app
import sys
import flask


try:
    gb.conn = apsw.Connection(gb.DATABASE_path)
    c = gb.conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id integer PRIMARY KEY, 
        sender TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        content TEXT NOT NULL,
        replyId integer,
        recipients TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS users ( 
        name TEXT NOT NULL PRIMARY KEY,
        hash binary(32),
        salt varbinary(16));''')
    
except Error as e:
    print(e)
    sys.exit(1)
