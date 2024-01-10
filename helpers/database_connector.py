import sqlite3

class SQLiteConnector:
    _instance = None
    
    def __new__(cls, database_path):
        if not cls._instance:
            cls._instance = super(SQLiteConnector, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(database_path)
            cls._instance.cursor = cls._instance.connection.cursor()
        return cls._instance

    def execute_query(self, query, parameters=None):
        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor

    def fetch_data_one(self, query, parameters=None):
        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()