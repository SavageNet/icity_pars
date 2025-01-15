from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from config import API_ID, API_HASH, PHONE, CHANNEL_USERNAME
from functions import contains_dash, split_by_dash, clear

# Введите свои API ID и API Hash
api_id = API_ID
api_hash = API_HASH
phone = PHONE
channel_username = CHANNEL_USERNAME

client = TelegramClient('session_1', api_id, api_hash)

async def main():
    offset_id = 0
    limit = 100  # Количество сообщений за один запрос
        
    await client.start()
    print('Client Created')

    # Убедитесь, что вы авторизованы
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
    
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
                    key = button['text']
                    value = int(button['url'].split('/')[-1])
                    if key not in product_msg_id:
                        product_msg_id[key] = value
    product_msg_list = await client.get_messages(channel_username, ids=list(product_msg_id.values()))
    result = {}
    msg_buffer = []
    for p, product_msg in enumerate(product_msg_list):
        if p > 3:
            break
        lines = product_msg.message.split('\n')
        line_name = lines[0]
        for i in range(len(lines)):
            if contains_dash(lines[i]):
                words = split_by_dash(lines[i])
                name = words[0]
                price = words[-1].strip()[:-1].replace('.', '')
                price = "{:,.0f}".format(int(price) - 1_000).replace(',', '.')
                lines[i] = ''.join([name, price, words[-1][-1]])
            msg_buffer.append(lines[i])
        result[line_name] = '\n'.join(msg_buffer)
        msg_buffer = []
    for line_name in result:
        print(result[line_name], end = '\n-----------------------------')
        
        #await client.send_message('appeler_store', result)        
        # i = 1
        # while i < len(lines):
        #     if contains_dash(lines[i]) and not contains_dash(lines[i - 1]):
        #         delta = 1
        #         while i - delta >= 0 and len(lines[i - delta].replace(' ', '').replace('\n', '')) == 0:
        #             delta += 1
        #         product_name = clear(lines[i - delta])
        #         result[product_name] = {}
        #         while i < len(lines) and contains_dash(lines[i]):
        #             words = split_by_dash(lines[i])
        #             product_type = clear(words[0])
        #             product_type_price = clear(words[-1])
        #             result[product_name][product_type] = product_type_price
        #             i += 1
        #     else: 
        #         i += 1
    # for key, value in result.items():
    #     print(f'{key}: {value}', end = '\n\n')

with client:
    client.loop.run_until_complete(main())
