import re
from functions import *

def simple_pars(lines: list[str], clear_func: callable, result: dict, goal_word='', skip_prefix='qwertyuiop'):
    i = 1
    while i < len(lines):
        if is_price_line(lines[i]) and not is_price_line(lines[i - 1]):
            delta = 1
            while i - delta > 0\
                and (len(clear(lines[i - delta])) == 0\
                     or goal_word.lower() not in clear(lines[i - delta]).lower()):
                delta += 1
            product_name = clear_func(lines[i - delta].strip())
            if product_name not in result:
                result[product_name] = {}
            while i < len(lines)\
                and (is_price_line(lines[i])\
                    or len(clear(lines[i])) == 0\
                    or lines[i].startswith(skip_prefix)):
                if is_price_line(lines[i]):
                    words = split_by_dash(lines[i])
                    product_type, product_type_price = tuple(map(lambda x: clear_func(x.strip()), words))
                    result[product_name][product_type] = product_type_price
                i += 1
        else: 
            i += 1
    return result

def playstation_pars(lines: list[str], clear_func: callable, result: dict, goal_word='', skip_prefix='qwertyuiop'):
    i = 1
    while i < len(lines):
        if is_price_line(lines[i]) and not is_price_line(lines[i - 1]):
            delta = 1
            while i - delta > 0\
                and (len(clear(lines[i - delta])) == 0\
                     or goal_word.lower() not in clear(lines[i - delta]).lower()):
                delta += 1
            product_name = clear_func(lines[i - delta].strip())
            if product_name not in result:
                result[product_name] = {}
            while i < len(lines)\
                and (is_price_line(lines[i])\
                    or len(clear(lines[i])) == 0\
                    or lines[i].startswith(skip_prefix)):
                if is_price_line(lines[i]):
                    words = split_by_dash(lines[i])
                    product_type, product_type_price = tuple(map(lambda x: clear_func(x.strip()), words))
                    delta = 0
                    if 'ESSENTIAL' in product_type:
                        delta = 1
                    elif 'EXTRA' in product_type:
                        delta = 2
                    elif 'DELUXE' in product_type:
                        delta = 3
                    if delta > 0:
                        product_type = product_type + f' ({lines[i - delta]})'
                    result[product_name][product_type] = product_type_price
                i += 1
        else: 
            i += 1
    return result
  
def get_data(lines: list[str], parser_type: str, need_cleaning=False):
    result = {}
    parser_type = parser_type.lower()
    simple_message_names = (
        'iphone',
        'macbook',
        'airpods',
        'ipad',
        'samsung',
        'vr',
        'garmin',
        'gopro',
        'dji',
        'аудио'
    )
    clear_func = clear if need_cleaning else lambda x: x
    is_simple = any([e.lower() in parser_type for e in simple_message_names])
    lines = list(map(lambda line: re.sub(r'\s+', ' ', line).replace(':', ''), lines))
    if is_simple:
        result = simple_pars(lines, clear_func, result)
    elif 'watch' in parser_type:
        result = simple_pars(lines, clear_func, result, goal_word='watch')
    elif 'imac' in parser_type:
        lines = list(map(
            lambda x: x.replace('[MCYT4] Mac Mini M4 (24/512) ', '[MCYT4] Mac Mini M4 (24/512) - '),
            lines
        ))
        result = simple_pars(lines, clear_func, result, skip_prefix='[')
    elif 'аксессуары' in parser_type:
        for i in range(len(lines)):
            if len(lines[i].strip()) > 0 and lines[i].strip().endswith('0'):
                lines[i] = lines[i].strip() + '₽'        
        adapter_index = find_in_list(lines, lambda line: 'adapter' in line.lower())
        if adapter_index > 0:
            lines[adapter_index - 1] = '🔌 Adapter'
        result = simple_pars(lines, clear_func, result, skip_prefix='(')      
    elif 'dyson' in parser_type:
        air_cleaner_index = find_in_list(lines, lambda line: 'увлажнитель-очиститель воздуха' in line.lower())
        if air_cleaner_index:
            lines[air_cleaner_index] = lines[air_cleaner_index] + ' Dyson'
        result = simple_pars(lines, clear_func, result, goal_word='dyson') 
    elif 'playstation' in parser_type:  
        for i in range(len(lines)):
            if lines[i].endswith('0р'):
                lines[i] = lines[i][:-2] + '0₽'          
        result = playstation_pars(lines, clear_func, result, goal_word='Sony PlayStation') 
    elif 'пылесос' in parser_type:
        for i in range(len(lines)):
            if len(lines[i].strip()) > 0 and lines[i].strip()[-1].isdigit():
                lines[i] = lines[i].strip() + '₽'
        result = simple_pars(lines, clear_func, result)
    else:
        return None
    return result