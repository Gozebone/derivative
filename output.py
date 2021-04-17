import re


def clear_expression(part):
    while checking_if_in_brackets(part):
        part = part[1:-1]

    part = part.replace('--', '+')
    part = part.replace('(+', '(')
    part = part.replace('*+', '*')
    part = part.replace('/+', '/')

    part_list = re.split('([+|-])', part)

    for element in range(len(part_list)):
        if element != '-' and element != '+':
            if element.find('+') != -1 and element.find('-') != -1:
                clear_expression(part)

    return part

def checking_if_in_brackets(part):
    part_len = len(part)-1
    if part[0] == '(' and part[part_len] == ')':
        brackets_count = 1
        for char_num in (1, part_len):
            if char_num == '(':
                brackets_count += 1
            elif char_num == ')':
                brackets_count -= 1

            if brackets_count == 0:
                return False

            return True

    else:
        return False

def split_with_separator(part):
    
