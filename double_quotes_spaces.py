#!/usr/bin/env python3

def double_quotes_spaces(path: str, mode: bool = True) -> str:
    """Double Quotes Spaces
    
    If the @path has spaces, function puts it between quotation marks
    Switch @mode, if:
    - True - puts all @path in quotation marks
    - False - puts only nodes w/spaces in quotation marks"""

    if ' ' not in path:
        return path

    if mode:
        return '"' + path + '"'

    path = path.split('\\')

    for i, j in enumerate(path):
        if ' ' in j:
            path[i] = f'"{j}"'

    return '\\'.join(path)

path2check = r'C:\Program Files\7-zip\Program Files\Program Files\7-zip\Program Fil'

print(double_quotes_spaces(path2check))
print(double_quotes_spaces(path2check, False))

path2check = r'C:\ProgramFiles\7-zip\ProgramFiles'

print(double_quotes_spaces(path2check))
print(double_quotes_spaces(path2check, False))
