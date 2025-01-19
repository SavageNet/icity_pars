from functions import *
import re

def get_data(lines: list[str], parser_type: str):
    result = {}
    parser_type = parser_type.lower()
    if 'iphone' in parser_type or 'macbook' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0:
                    delta += 1
                product_name = lines[i - delta]
                result[product_name.strip()] = {}
                while i < len(lines) and is_price_line(lines[i]):
                    words = split_by_dash(lines[i])
                    product_type = words[0]
                    product_type_price = clear(words[-1])
                    result[product_name.strip()][product_type.strip()] = product_type_price
                    i += 1
            else: 
                i += 1  
    elif 'airpods' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0:
                    delta += 1
                product_name = lines[i - delta]
                if len(result) == 0:
                    while i < len(lines) and is_price_line(lines[i]):
                        words = split_by_dash(lines[i])
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        result[product_type] = {}
                        result[product_type]['-'] = product_type_price
                        i += 1
                else:
                    result[product_name.strip()] = {}
                    while i < len(lines) and is_price_line(lines[i]):
                        words = split_by_dash(lines[i])
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        result[product_name.strip()][product_type.strip()] = product_type_price
                        i += 1
            else: 
                i += 1
    elif 'watch' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0 or 'watch' not in lines[i - delta].lower():
                    delta += 1             
                product_name = lines[i - delta]
                result[product_name.strip()] = {}
                while i < len(lines) and is_price_line(lines[i]):
                    words = split_by_dash(lines[i])
                    product_type = words[0]
                    product_type_price = clear(words[-1])
                    result[product_name.strip()][product_type.strip()] = product_type_price
                    i += 1
            else: 
                i += 1  
    elif 'ipad' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0:
                    delta += 1
                product_name = lines[i - delta]
                if len(result) == 0:
                    result['Apple Pencil'] = {}
                    while i < len(lines) and is_price_line(lines[i]):
                        words = list(map(
                            lambda word: word.replace('USB_C', 'USB-C'),
                            split_by_dash(lines[i].replace('USB-C', 'USB_C')))
                        )
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        result['Apple Pencil'][product_type.strip()] = product_type_price
                        i += 3
                else:
                    result[product_name.strip()] = {}
                    while i < len(lines) and (is_price_line(lines[i]) or len(clear(lines[i])) == 0):
                        if not len(clear(lines[i])) == 0:
                            words = list(map(
                                lambda word: word.replace('Wi_Fi', 'Wi-Fi'),
                                split_by_dash(lines[i].replace('I', 'i').replace('Wi-Fi', 'Wi_Fi')))
                            )
                            product_type = words[0]
                            product_type_price = clear(words[-1])
                            result[product_name.strip()][product_type.strip()] = product_type_price
                        i += 1
            else: 
                i += 1  
    elif 'imac' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0:
                    delta += 1
                product_name = lines[i - delta]
                if not '(' in product_name:
                    result[product_name.strip()] = {}
                    while i < len(lines) and (is_price_line(lines[i]) or lines[i].startswith('[')):
                        if not lines[i].startswith('['): 
                            words = split_by_dash(lines[i])
                            product_type = words[0]
                            product_type_price = clear(words[-1])
                            result[product_name.strip()][product_type.strip()] = product_type_price
                        i += 1
                else:
                    product_name, product_type = list(map(
                        lambda x: x.replace(')', '').strip(),
                        product_name.split('('))
                    )
                    if product_name not in result: 
                        result[product_name.strip()] = {}
                    while i < len(lines) and is_price_line(lines[i]):
                        words = split_by_dash(lines[i])
                        product_type_price = clear(words[-1])
                        result[product_name.strip()][product_type.strip()] = product_type_price
                        i += 1                    
            else: 
                i += 1  
    elif 'аксессуары' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i]) and 'pencil' not in lines[i].lower()
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0:
                    delta += 1
                product_name = lines[i - delta].replace('🔌 Аксессуары Apple 🔌', '🥽 Apple Vision Pro').replace(':', '').strip()
                if 'Pack' in product_name:
                    product_name = '🔌 Adapter'
                result[product_name.strip()] = {}
                while i < len(lines) and is_price_line(lines[i]):
                    words = split_by_dash(lines[i])
                    product_type = words[0]
                    product_type_price = clear(words[-1])
                    result[product_name.strip()][product_type.strip()] = product_type_price
                    i += 1
            else: 
                i += 1         
    elif 'samsung' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0:
                    delta += 1
                product_name = lines[i - delta]
                result[product_name.strip()] = {}
                while i < len(lines) and (is_price_line(lines[i]) or len(clear(lines[i])) == 0):
                    if not len(clear(lines[i])) == 0:
                        words = split_by_dash(lines[i])
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        result[product_name.strip()][product_type.strip()] = product_type_price
                    i += 1
            else: 
                i += 1
    elif 'playstation' in parser_type:
        lines = list(map(
            lambda line: line\
                .replace('( Турция - 🇹🇷 )', '')\
                .replace('Подписки Sony PlayStation Plus Турция 🇹🇷', '')\
                .replace('Подписка Sony PlayStation Plus', 'Подпискa Sony PlayStation Plus Турция 🇹🇷'),
            lines
        ))
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0:
                    delta += 1
                product_name = lines[i - delta]
                result[product_name.strip()] = {}
                while i < len(lines) and \
                    (is_price_line(lines[i]) \
                        or len(clear(lines[i])) == 0 \
                        or 'месяц' in lines[i]):
                    if (not len(clear(lines[i])) or 'месяц' in lines[i].lower()) == 0:
                        line = lines[i]
                        if 'essential' in lines[i].lower():
                            line = line.replace(' - ', f' {lines[i - 1]} - ')
                        if 'extra' in lines[i].lower():
                            line = line.replace(' - ', f' {lines[i - 2]} - ')
                        if 'deluxe' in lines[i].lower():
                            line = line.replace(' - ', f' {lines[i - 3]} - ')
                        words = split_by_dash(line)
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        if not product_type_price[-1].isdigit():
                            product_type_price = product_type_price[:-1]
                        result[product_name.strip()][product_type.strip()] = product_type_price
                    i += 1
            else: 
                i += 1
    elif 'dyson' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and (len(clear(lines[i - delta])) or lines[i - delta].startswith('(')) == 0:
                    delta += 1
                product_name = lines[i - delta]
                result[product_name.strip()] = {}
                while i < len(lines) and (is_price_line(lines[i]) or len(clear(lines[i])) == 0):
                    if not len(clear(lines[i])) == 0:
                        line = re.sub(r'\s+', ' ', lines[i]).replace(' )', ')')
                        words = split_by_dash(line)
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        result[product_name.strip()][product_type.strip()] = product_type_price
                    i += 1
            else: 
                i += 1
    elif 'gopro' in parser_type:
        i = 1
        while i < len(lines):
            curr_line = lines[i]
            prev_line = lines[i - 1]
            flag1 = is_price_line(lines[i])
            flag2 = is_price_line(lines[i - 1])
            if flag1 and not flag2:
                delta = 1
                while i - delta >= 0 and len(clear(lines[i - delta])) == 0:
                    delta += 1
                product_name = lines[i - delta]
                result[product_name.strip()] = {}
                while i < len(lines) and is_price_line(lines[i]):
                    words = split_by_dash(lines[i])
                    product_type = words[0]
                    product_type_price = clear(words[-1])
                    result[product_name.strip()][product_type.strip()] = product_type_price
                    i += 1
            else: 
                i += 1          
    else:
        return None
    return result