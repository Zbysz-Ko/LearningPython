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

    for i in range(len(path)):
        if ' ' in path[i]:
            path[i] = '"' + path[i] + '"'

    return '\\'.join(path)

path = r'C:\Program Files\7-zip\Program Files\Program Files\7-zip\Program Fil'

print(double_quotes_spaces(path))
print(ddouble_quotes_spaces(path, False))

path = r'C:\ProgramFiles\7-zip\ProgramFiles'

print(double_quotes_spaces(path))
print(double_quotes_spaces(path, False))
