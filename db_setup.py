import sqlite3

def creat_connection():
	conn = sqlite3.connect('mybot.db')
	return conn
	
	
def creat_table():
	conn = creat_connection()
	cursor = conn.cursor()
	
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS user (
	  id INTEGER PRIMARY KEY,
	  user_id INTEGER UNIQUE,
	  username TEXT,
	  first_name TEXT,
	  refrralcode TEXT UNIQUE,
   token_recive TEXT DEFAULT NULL,
	  points INTEGER DEFAULT 20
	)
	''')
	
	conn.commit()
	conn.close()
	
if __name__ == '__main__':
	creat_table()
