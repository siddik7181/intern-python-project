import sqlite3
from contextlib import contextmanager

@contextmanager
def createdb(filename="mydb.db", table="tweets", schema="id INTEGER PRIMARY KEY AUTOINCREMENT, tweet TEXT"):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
    yield cursor
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
    if cursor:
        cursor.close()
    if connection:
        connection.commit()
        connection.close()

class UniquenessChecker:
    def __init__(self, cursor, table, column, column_value):
        self.cursor = cursor
        self.table = table
        self.column = column
        self.column_value = f'"{column_value}"'


    def __enter__(self):

        query = f"SELECT 1 FROM {self.table} WHERE {self.column} = {self.column_value} "
        print(f"Query: {query}")
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if res:
            raise ValueError('Duplicate value!!, value already exist in the database')
        return self.column_value

    def __exit__(self, *args, **kwargs):
        pass

def addData(cursor, table, column, column_value):

    with UniquenessChecker(cursor, table, column, column_value) as new_column_value:

        query = f"INSERT INTO {table} ({column}) VALUES ({new_column_value})"
        cursor.execute(query)
        print(f"Successfully added new row to {table}.")
