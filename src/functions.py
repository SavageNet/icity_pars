import re

def is_price_line(line: str) -> bool:
    line = line.strip()
    endings = ('ожидаем', 'по запросу', 'ревизия)', 'уточняйте')
    return ('-' in line or '–' in line) and (line[-2].isdigit() or line.endswith(endings))


def split_by_dash(line: str) -> list[str]:
    if chr(45) in line:
        result = line.split(chr(45))
        if len(result) > 2:
            raise Exception(f'В строке больше одного тире: {result}')
    else:
        result = line.split(chr(8211))
        if len(result) > 2:
            raise Exception(f'В строке больше одного тире: {result}')        
    return result

def clear(line: str) -> str:
    result = re.sub(r'[^а-яА-ЯёЁa-zA-Z0-9(){}\[\]\-\–\+\”\".;,\/ ]', '', line)
    result = re.sub(r'\s+', ' ', result)
    result = re.sub(r'\s*;\s*', ';', result)
    return result.strip() 

def is_right_key(key: str, product_list: list[str]) -> bool:
    for product in product_list:
        if product.lower().replace(' ', '') in key.lower().replace(' ', ''):
            return True 
    return False

def print_dict(d: dict):
    for key, value in d.items():
        print(f'{key}: {value}')
