import psycopg2
from config import *

try:
    # Установите соединение с базой данных
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_username,
        password=db_password,
        host='localhost',
        port='5432'
    )
    if conn: 
        print(f'Connected to {db_name}')
    with conn.cursor() as cursor:
        query = """
            select * from test
        """
        cursor.execute(query)
        records = cursor.fetchall()
        
        for row in records:
            print(row)
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    if conn:
        conn.close()
