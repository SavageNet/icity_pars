from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import json
import os
from config import *
from functions import *
from parser import *

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
        if message.pinned and 'розыгрыш' not in message.message.lower():
            message = message.to_dict()
            for element in message['reply_markup']['rows']:
                for button in element['buttons']:
                    key = clear(button['text']).lower().replace(' ', '')
                    value = int(button['url'].split('/')[-1])
                    if product_list == None or any([name.lower() in key.lower() for name in product_list]):
                        product_msg_id[key] = value
    product_msg_list = await client.get_messages(channel_username, ids=list(product_msg_id.values()))
    return product_msg_list

def save_json(product_msg_list, json_name):
    result = []
    for _, product_msg in enumerate(product_msg_list):
        if not product_msg.message: 
            continue 
        msg_text = product_msg.message
        lines = msg_text.split('\n')
        if 'Гонконг / Китай' in lines[0]: 
                continue
        data = get_data(lines, parser_type=lines[0], need_cleaning=False)
        if data:
            result.append(data)
        else:
            raise Exception(f'break на {lines[0]}')
    with open(f'data/{json_name}.json', 'w') as json_file:
        json.dump(result, json_file, ensure_ascii=True, indent=4, )
        print(f'Сохранил {json_name}.json в {os.path.abspath('data/')}')

async def main():
    product_msg_list = await get_right_messages(channel_username, product_list=product_list)
    my_product_msg_list = await get_right_messages(my_channel_username, product_list=product_list)
    save_json(product_msg_list, 'icity_data')
    save_json(my_product_msg_list, 'appler_data')

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
