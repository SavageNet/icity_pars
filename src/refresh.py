import psycopg2
import json
from config import *
import re

def get_connect(db_name, db_username, db_password, host, port):
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_username,
        password=db_password,
        host=host,
        port=port
    )
    if not conn: 
        raise Exception('ConnectionError')
    return conn

def main():
    try:
        conn = get_connect(db_name, db_username, db_password, host, port)   
        with conn.cursor() as cursor:
            with open('database/stg.delta_price_insert.sql', 'r') as query:
                cursor.execute(query.read())
                conn.commit()
                print(f'Insert for table stg.delta_price was exicuted')
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
        
if __name__ == '__main__':
    main()
    
    