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
    with conn.cursor() as cursor:
        query = """
            select * from pg_roles
        """
        cursor.execute(query)
        records = cursor.fetchall()
        
        for row in records:
            print(row)
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    if conn: conn.close()
