import psycopg2
import json
import os
import sys
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
from src.config import *

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

def get_query(json_name, table_schema, table_name):
    with open(f'data/{json_name}.json', 'r') as file:
        data = json.load(file)
        query_lines = []
        for product_data in data:
            for model_nm, feature_dict in product_data.items():
                for model_feature, price in feature_dict.items():
                    price = price.replace('.', '')
                    try: 
                        price = int(price)
                    except:
                        price = 'NULL'
                    query_lines.append(f'(\'{model_nm}\', \'{model_feature}\', {price})')
    values_str = ', '.join(query_lines)
    query = f"""
        TRUNCATE TABLE {table_schema}.{table_name} RESTART IDENTITY
        ;
        insert into {table_schema}.{table_name}(model_name, model_feature, price)
        values
        """
    query = query + values_str        
    return query

def main():
    icity_query = get_query(
        json_name='icity_data',
        table_schema='source',
        table_name='icity_price'
    )
    appler_query = get_query(
        json_name='appler_data',
        table_schema='source',
        table_name='appler_price'       
        )
    try:
        conn = get_connect(db_name, db_username, db_password, host, port)   
        with conn.cursor() as cursor:
            cursor.execute(icity_query)
            cursor.execute(appler_query)
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
        
if __name__ == '__main__':
    main()
    