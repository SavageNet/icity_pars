import re

def contains_dash(line: str) -> bool:
    return chr(45) in line or chr(8211) in line

def split_by_dash(line: str) -> list[str]:
    if chr(45) in line:
        return line.split(chr(45))
    else:
        return line.split(chr(8211))

def clear(line: str) -> str:
    result = re.sub(r'[^a-zA-Z0-9(){}\[\] ]', '', line)
    result = re.sub(r'\s+', ' ', result)
    return result.strip() 