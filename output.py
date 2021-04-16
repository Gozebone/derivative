def clear_expression(part):
    part = part.replace('--', '+')
    part = part.replace('(+', '(')
    part = part.replace('*+', '*')
    part = part.replace('/+', '/')
    return part
