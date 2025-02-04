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
    Функция разделит строку по первому дефису слева от цены. Или по первому пробелу, если дефиса нет (Выдаст предупреждение в таком случае) 
    Не учитывает ₽ и все после него!
    """
    if (rub_index := line.find('₽')) != -1:
        line = line[:rub_index]
    line = line.strip()
    last_space_index = None
    for i in range(len(line) - 1, -1, -1):
        if line[i] == ' ':
            last_space_index = i
            break
    else:
        raise Exception(f'Сломалось на: {line}')
    try:
        if re.match(r'[\-|\–]', line[last_space_index + 1]):
            last_space_index += 1
        elif re.match(r'[\-|\–]', line[last_space_index - 1]):
            last_space_index -= 1
        result = (line[:last_space_index], line[last_space_index + 1:])
        if line[last_space_index] != '-':
            print(f'WARNING! Ебанутая строка {line}. Разделилась как {result}')
        return result
    except Exception as e:
        print(f'WARNING {e} at line {line}')
        return (line[:last_space_index], None)
        

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
