import re

def is_price_line(line: str) -> bool:
    specific_strings = ('ожидаем', 'по запросу', 'уточняйте', '💛')
    ban_strings = ('(Актуальные цены уточняйте)',)
    is_specific_line = any([e.lower() in line.lower() for e in specific_strings])
    a = [e.lower() in line.lower() for e in ban_strings]
    if any([e.lower() in line.lower() for e in ban_strings]):
        return False
    return '₽' in line or is_specific_line

def split_by_dash(line: str) -> tuple[str]:
    """
    Функция разделит строку по первому дефису слева от цены. 
    Не учитывает ₽ и все после него!
    """
    if not (rub_index := line.find('₽')) == -1:
        line = line[:rub_index]
    dash_index = None
    for i in range(len(line) - 1, -1, -1):
        if line[i] == chr(45) or line[i] == chr(8211):
            dash_index = i
            break
    else:
        raise Exception(f'В строке нет дефиса: {line}')
    try:
        return (line[:dash_index], line[dash_index + 1:])
    except Exception as e:
        print(f'WARNING {e} at line {line}')
        return (line[:dash_index], None)
        

def clear(line: str) -> str:
    result = re.sub(r'[^а-яА-ЯёЁa-zA-Z0-9\(\)\{\}\[\]\-\–\+\”\".;,\/ ]', '', line)
    result = re.sub(r'\s+', ' ', result)
    result = re.sub(r'\s*;\s*', ';', result)
    return result.strip() 

def find_in_list(list: list, condition: callable):
    for i in range(len(list)):
        if condition(list[i]):
            return i
    return None

def print_dict(d: dict):
    for key, value in d.items():
        print(f'{key}: {value}')
