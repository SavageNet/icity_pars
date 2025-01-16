from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from config import *
from functions import *
from parser import *

client = TelegramClient('session_1', api_id, api_hash)

async def get_right_messages(channel_username: str, product_list: list[str] = None, offset_id:int = 0, limit:int = 100):
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
                    if product_list == None or is_right_key(key, product_list):
                        product_msg_id[key] = value
    product_msg_list = await client.get_messages(channel_username, ids=list(product_msg_id.values()))
    return product_msg_list, product_msg_id

async def main():
    product_msg_list, product_msg_id = await get_right_messages(channel_username, product_list=product_list)
    my_product_msg_list, my_product_msg_id = await get_right_messages(my_channel_username, product_list=product_list)    
    result = {}
    msg_buffer = []
    for _, product_msg in enumerate(product_msg_list):
        if not product_msg.message: 
            continue 
        lines = product_msg.message.split('\n')
        data = get_data(lines, parser_type = lines[0])
        if data:
            print_dict(data)
            print('\n--------------------------------\n')
        else:
            break
with client:
    client.loop.run_until_complete(main())
