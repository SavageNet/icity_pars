from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors.rpcerrorlist import MessageNotModifiedError
import psycopg2
import regex
import time
from datetime import date
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
            pinned_message_id = message.id
            message = message.to_dict()
            for element in message['reply_markup']['rows']:
                for button in element['buttons']:
                    key = clear(button['text']).lower().replace(' ', '')
                    value = int(button['url'].split('/')[-1])
                    if product_list == None or any([name.lower() in key.lower() for name in product_list]):
                        product_msg_id[key] = value
    product_msg_list = await client.get_messages(channel_username, ids=list(product_msg_id.values()))
    return product_msg_list, pinned_message_id

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
    try:
        conn = get_connect(db_name, db_username, db_password, host, port)
        result = {}   
        with conn.cursor() as cursor:
            cursor.execute('select model_name, model_features, prices from dm.message_compile')
            rows = cursor.fetchall()
            conn.commit()
            for model_name, model_features, prices in rows:
                if model_name not in result:
                    model_features = model_features.split(';')
                    prices = prices.split(';')
                    result[model_name] = {model_feature: price for model_feature, price in zip(model_features, prices)}
                else:
                    raise Exception()
            
            return result
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

async def rewrite_messages(messages_by_id: dict[int, str], data: dict[str,dict[str,str]], pinned_message_id):
    channel_entity = await client.get_entity(my_channel_username)
    for message_id, message_text in messages_by_id.items():
        lines = message_text.split('\n')
        for i in range(len(lines)):
            if len(lines[i]) > 0 and lines[i][0] == '-':
                lines[i] = lines[i][1:]
        is_found = [False for _ in lines]
        for model_name, price_lines_dict in data.items():
            model_name = regex.sub(r'(?<=Увлажнитель-очиститель воздуха).+', '', model_name)
            model_name_index = find_in_list(lines,
                lambda line: clear(line) == clear(model_name),
                is_found_list=is_found
            )
            if clear(lines[0]) == 'Аксессуары' and model_name == '🔌 Adapter':
                model_name_index = find_in_list(lines,
                    lambda line: clear(line).startswith('Adapter 20w'),
                    is_found_list=is_found
                )
                model_name_index -= 1           
            if model_name_index is not None: 
                is_found[model_name_index] = True
                price_lines_dict_items = price_lines_dict.items()
                if clear(lines[0]) == 'Sony PlayStation' and model_name.startswith('Подписки Sony PlayStation Plus'):
                    price_lines_dict_items = sorted(price_lines_dict.items(), key=lambda pair: int(re.search(r'(?<=\()\d+', pair[0]).group()))
                for model_feature, price in price_lines_dict_items:
                    model_feature = regex.sub(r'(?<=DELUXE|EXTRA|ESSENTIAL).+', '', model_feature)
                    price_line_index = find_in_list(lines,
                         lambda line: clear(line).startswith(clear(model_feature)),
                         start_index=model_name_index,
                         is_found_list=is_found
                    )
                    if price_line_index is None: 
                        raise Exception(f'Не нашел {model_feature} в сообщении {lines[0]} после {model_name}')
                    is_found[price_line_index] = True
                    if price == '-1':
                        lines[price_line_index] = f'{model_feature} - ожидаем'
                    else:
                        lines[price_line_index] = f'{model_feature} - {'{:,.0f}'.format(int(price)).replace(',', '.')}₽'
        with open(f'file_{message_id}.txt', 'w', encoding='UTF-8') as file:
            file.write('\n'.join(lines))
        try:
            await client.edit_message(channel_entity, message_id, '\n'.join(lines))
            print(f'Message {lines[0]} was edited')
        except MessageNotModifiedError:
            print(f'WARNING Message {lines[0]} was remained')
        finally:
            time.sleep(1)
    try:    
        pinned_message = await client.get_messages(my_channel_username, ids=pinned_message_id)
        pinned_message_text = pinned_message.message
        current_date = date.today().strftime("%d.%m.%y")
        pinned_message_text = re.sub(r'\d\d.\d\d.\d\d', current_date, pinned_message_text)
        await client.edit_message(channel_entity, pinned_message_id, pinned_message_text)
        print('Date was edited')
    except MessageNotModifiedError:
        print('Date date was remained')

            
        
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
    product_msg_list, pinned_message_id = await get_right_messages(my_channel_username, product_list=product_list)
    data = get_content_from_view()
    messages_by_id = {product_msg.id: product_msg.message for product_msg in product_msg_list}
    await rewrite_messages(messages_by_id, data, pinned_message_id)
     
with client:
    client.loop.run_until_complete(main())