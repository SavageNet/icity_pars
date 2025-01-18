from functions import *

def get_data(lines: list[str], parser_type: str):
    result: dict[str, dict[str, str]] = {}
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
                result[product_name] = {}
                while i < len(lines) and is_price_line(lines[i]):
                    words = split_by_dash(lines[i])
                    product_type = words[0]
                    product_type_price = clear(words[-1])
                    result[product_name][product_type] = product_type_price
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
                        result[product_type]['default'] = product_type_price
                        i += 1
                else:
                    result[product_name] = {}
                    while i < len(lines) and is_price_line(lines[i]):
                        words = split_by_dash(lines[i])
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        result[product_name][product_type] = product_type_price
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
                result[product_name] = {}
                while i < len(lines) and is_price_line(lines[i]):
                    words = split_by_dash(lines[i])
                    product_type = words[0]
                    product_type_price = clear(words[-1])
                    result[product_name][product_type] = product_type_price
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
                            split_by_dash(lines[i].replace('USB-C', 'USB_C'))))
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        result['Apple Pencil'][product_type] = product_type_price
                        i += 3
                else:
                    result[product_name] = {}
                    while i < len(lines) and (is_price_line(lines[i]) or len(clear(lines[i])) == 0):
                        if len(clear(lines[i])) == 0:
                            i += 1 
                            continue
                        words = list(map(
                            lambda word: word.replace('Wi_Fi', 'Wi-Fi'),
                            split_by_dash(lines[i].replace('I', 'i').replace('Wi-Fi', 'Wi_Fi'))))
                        product_type = words[0]
                        product_type_price = clear(words[-1])
                        result[product_name][product_type] = product_type_price
                        i += 1
            else: 
                i += 1         
    else:
        return None
    return result