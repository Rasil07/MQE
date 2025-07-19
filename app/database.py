from app.config import Config
import sqlite3
import os

class Database:
    def __init__(self, db_path):
        # Check if the database file exists at the specified path if not create it
        if not os.path.exists(db_path):
            with open(db_path, 'w') as f:
                f.write('')
                print(f"Database file created at {db_path}")
        self.db_path = db_path
        

    def initialize_tables(self,db_schema):    
        with open(db_schema, 'r') as f:
            cur =self.connect()
            cur.executescript(f.read())
            cur.commit()
            cur.close()
    
    def connect(self):
        print(f"Connecting to database at {self.db_path}")
        return sqlite3.connect(self.db_path)
        

    def run(self,query, args=(), one=False):
        cur = self.connect().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
