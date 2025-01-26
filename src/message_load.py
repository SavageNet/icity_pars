from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
import psycopg2
from config import *
from functions import *

client = TelegramClient('session_1', api_id, api_hash)

async def get_right_messages(channel_username: str, product_list: list[str] = None, offset_id:int = 0, limit:int = 100, client=client):
    channel = await client.get_entity(channel_username)
    history = await client(GetHistoryRequest(
        peer=channel,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))  
    messages = history.messages
    product_msg_id = {}
    for message in messages:
        if message.pinned:
            message = message.to_dict()
            for element in message['reply_markup']['rows']:
                for button in element['buttons']:
                    key = clear(button['text']).lower().replace(' ', '')
                    value = int(button['url'].split('/')[-1])
                    if product_list == None or any([name.lower() in key.lower() for name in product_list]):
                        product_msg_id[key] = value
    product_msg_list = await client.get_messages(channel_username, ids=list(product_msg_id.values()))
    return product_msg_list, product_msg_id

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

def get_content_from_view():
    

async def main():
    product_list = [
        'Iphone', 
        'Airpods', 
        'Watch', 
        'MacBook', 
        'IPad', 
        'IMac', 
        'Аксессуары', 
        'Samsung', 
        'Dyson', 
        'Play', 
        'Камер'
    ]    
    product_msg_list, product_msg_id = await get_right_messages(channel_username, product_list=product_list)
    try:
        conn = get_connect(db_name, db_username, db_password, host, port)   
        with conn.cursor() as cursor:
            cursor.execute(
                
            )
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
        
if __name__ == '__main__':
    client.loop.run_until_complete(main())