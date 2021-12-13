import psycopg2
from psycopg2.extras import RealDictCursor
from time import time

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi',
        user = 'postgres', password = '5spaces', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful!")
        break
    except Exception as error:
        print("Connection failed!")
        print("Error: ", error)
        time.sleep(2)

def get_cursor():
    return cursor