import sqlite3
import os

from settings import settings

class SQLite_Maneger:
    
    def __init__(self, db_path: str):
        self.db_path = os.path.join(settings.SQLITE_FILES_PATH,db_path)
        if os.path.exists(self.db_path):
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
        else:
            raise ValueError("This table does not exist!")
    
    def test(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM ORDERS;")
        results=cursor.fetchall()
        results_dict=[dict(row) for row in results if row is not None]
       
        for row in results_dict:
            print(row)
    
    def add(self,table,values):
        add_query =  f"INSERT INTO {table} VALUES {values}"
        cursor = self.conn.cursor()
        cursor.execute(add_query)
        self.conn.commit()
    
    def retrieve(self,columns,table,filter_column,filter_value):
        
        retrieve_query =  f"SELECT {columns} FROM {table} WHERE {filter_column} = ?"
        cursor = self.conn.cursor()
        cursor.execute(retrieve_query, (filter_value,))
        results=cursor.fetchall()
        results_dict=[dict(row) for row in results if row is not None]
        return results_dict
    
    def update(self,table,column,filter_column,new_value,filter_value):
        update_query =  f"UPDATE {table} SET {column} =?  WHERE {filter_column} = ?"
        cursor = self.conn.cursor()
        cursor.execute(update_query, (new_value,filter_value,))
        self.conn.commit()
        
    def remove(self,table,filter_column,filter_value):
        remove_query =  f"DELETE FROM {table} WHERE {filter_column} = ?"
        cursor = self.conn.cursor()
        cursor.execute(remove_query, (filter_value,))

    def commit_and_close(self):
        self.conn.commit()
        self.conn.close()
        

