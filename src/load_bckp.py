import psycopg2
from config import *
from functions import *

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

def get_query(table_schema, table_name):   
    with open(f'C:\\Users\\for_g\\Documents\\Dev\\ICITY_pars\\data\\appler_price_24.01 copy.csv', 'r', encoding='UTF8') as file:
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].replace('\n', '').split(';')
        query_lines = []
        for model_nm, model_feature, price, unit_nm in data[1:]:
            try: 
                price = int(price)
            except:
                price = 'NULL'
            query_lines.append(f'(\'{model_nm}\', \'{model_feature}\', {price})')
    values_str = ', '.join(query_lines)
    query = f"""
        TRUNCATE TABLE {table_schema}.{table_name}
        ;
        insert into {table_schema}.{table_name}(model_name, model_feature, price)
        values
        """
    query = query + values_str        
    return query

def main():
    appler_query = get_query(
        table_schema='source',
        table_name='appler_price_bckp_20250125'       
        )
    try:
        conn = get_connect(db_name, db_username, db_password, host, port)   
        with conn.cursor() as cursor:
            cursor.execute(appler_query)
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    with open('C:\\Users\\for_g\\Documents\\Dev\\ICITY_pars\\data\\appler_price_24.01.csv', 'r', encoding='UTF-8') as file:
        lines = file.readlines()       
        lines = list(map(
            lambda x: clear(x) + '\n',
            lines
        ))
        with open('C:\\Users\\for_g\\Documents\\Dev\\ICITY_pars\\data\\appler_price_24.01 copy.csv', 'w', encoding='UTF-8') as file_r:
            for line in lines:
                file_r.write(line)     
    main()
    print('Data is loaded')