from app.config import Config
import sqlite3
import os
from app.protocols import DatabaseProtocol
class Database(DatabaseProtocol):
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
        return sqlite3.connect(self.db_path)
    

    def run(self, query, args=(), commit=False, fetch_one=False, fetch_all=False):
        """
        Execute a SQLite query with the given arguments.
        
        Args:
            query (str): The SQL query to execute.
            args (tuple): The arguments to pass to the query (default: empty tuple).
            commit (bool): Whether to commit the transaction (default: False).
            fetch_one (bool): Whether to fetch only one result (default: False).
            fetch_all (bool): Whether to fetch all results (default: False).
            
        Returns:
            If fetch_one is True, returns a single row or None if no results.
            If fetch_all is True, returns all rows as a list.
            If neither, returns None.
        """
        conn = self.connect()
        conn.row_factory = sqlite3.Row  
        result = None
        try:
            cur = conn.execute(query, args)
            if commit:
                conn.commit()
            if fetch_one:
                row = cur.fetchone()
                result = dict(row) if row else None
            elif fetch_all:
                rows = cur.fetchall()
                result = [dict(row) for row in rows]
            else:
                result = None
            cur.close()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()
