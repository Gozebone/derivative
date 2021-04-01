
from collections import namedtuple


def function_finder(part):
    functions = [
        'sin',
        'cos',
        'tan',
        'ctg',
        'log',
        'ln(',
        'exp'
    ]

    for name in range(len(functions)):
        if part.find(functions[name]) != -1:
            return True

    return False


def pow_func(part):
    if part.find('(') != -1:
        brackets = 0
        for element in range(len(part)):
            if part[element] == '(':
                brackets += 1
            elif part[element] == ')':
                brackets -= 1
            if brackets == 0 and part[element] == '^':
                return True
    return False


def brackets_counter(element, inside, part):
    element += 4
    brackets = 1
    while brackets != 0:  # part[i] != ')' cos(x)+sin(cos(x)) -sin(x)+cos(cos(x)))*-sin(x)
        if part[element] == '(':
            brackets += 1
        elif part[element] == ')':
            brackets -= 1
        if brackets != 0:
            inside += part[element]
        element += 1
        # print(inside)
    if inside.isnumeric():
        inside_derivative = 1
    else:
        inside_derivative = der(inside)
    result = namedtuple("result", ["element", "inside", "inside_derivative"])
    return result(
        element,
        inside,
        inside_derivative
    )


def sing_finder(pos):
    global expression
    plus_couinter = 0
    part = ''
    # brackets = False
    for element in range(len(expression)):
        part += expression[element]
        if expression[element] == "+" or expression[element] == "-":  # and brackets == False:
            plus_couinter += 1
            if plus_couinter == pos:
                part = part[:-1]
                return part
            else:
                part = expression[element]
        elif element == len(expression) - 1:
            return part
        # elif expression[i] == "(":
        # brackets = True
        # elif expression[i] == ")":
        # brackets = False


def separate(part, separator):
    expressions = ['', '']

    for element in range(0, len(part)):

        if part[element] == separator:

            for j in range(element + 1, len(part)):
                expressions[1] += part[j]

            der_1 = der(expressions[0])
            der_2 = der(expressions[1])

            return str(f'({der_1}{separator}{der_2})')

        expressions[0] += part[element]

    return part


def sign_multiply(part):
    expressions = ['', '']

    for element in range(0, len(part)):

        if part[element] == '*':

            for j in range(element + 1, len(part)):
                expressions[1] += part[j]

            der_1 = der(expressions[0])
            der_2 = der(expressions[1])

            return str(f' ({der_1} * {expressions[1]} + {expressions[0]} * {der_2})')

        expressions[0] += part[element]

    return part


def sign_div(part):
    expressions = ['', '']

    for element in range(0, len(part)):

        if part[element] == '/':

            for j in range(element + 1, len(part)):
                expressions[1] += part[j]

            der_1 = der(expressions[0])
            der_2 = der(expressions[1])

            return str(f' (( {der_1} * {expressions[1]} - {expressions[0]} * {der_2})/( {expressions[1]} )^2)')

        expressions[0] += part[element]

    return part


def der(part):
    ans = ''

    # проверка на внешние скобки
    while part[0] == '(' and part[len(part) - 1] == ')':
        temp = ''
        brackets = 1
        for element in range(1, len(part) - 1):
            if part[element] == '(':
                brackets += 1
            elif part[element] == ')':
                brackets -= 1
            if brackets == 0:
                break
        if brackets == 0:
            break
        else:
            for element in range(1, len(part) - 1):
                temp += part[element]
            part = temp

    # проверка знака
    sign = '+'
    if part[0] == '-' or part[0] == '+':
        sign = part[0]
        # print("знак: " + sign)
        part = part[1:]
    if sign == '+':
        sign = ''

    # разделение по плюсу
    brackets = 0
    for element in range(0, len(part)):
        if part[element] == '(':
            brackets += 1
        elif part[element] == ')':
            brackets -= 1
        if part[element] == '+' and brackets == 0:
            ans = separate(part, '+')
            return ans

    # разделение по минусу
    brackets = 0
    for element in range(0, len(part)):
        if part[element] == '(':
            brackets += 1
        elif part[element] == ')':
            brackets -= 1
        if part[element] == '-' and brackets == 0:
            ans = separate(part, '-')
            return ans

    # проверка члена на умножение
    brackets = 0
    for element in range(len(part)):
        if part[element] == '(':
            brackets += 1
        elif part[element] == ')':
            brackets -= 1
        if part[element] == '*' and brackets == 0:
            ans = sign_multiply(part)
            return ans

    # проверка члена на деление
    brackets = 0
    for element in range(0, len(part)):
        if part[element] == '(':
            brackets += 1
        elif part[element] == ')':
            brackets -= 1
        if part[element] == '/' and brackets == 0:
            ans = sign_div(part)
            return ans



    # проверка наличия функция sin cos tan ctg
    lit = ''  # код функции
    for element in range(0, len(part)):
        if function_finder(part) and not part[element].isnumeric():
            if (part.find('^') != -1 and not pow_func(part)) or part.find('^') == -1:
                lit += part[element]
                lit += part[element + 1]
                lit += part[element + 2]
                break

    # --------------------------------------------------------------------------------------------------------
    # проверка Синуса

    if lit == 'sin':
        inside = inside_derivative = const = ''

        # отдаление константы
        for element in range(0, len(part)):
            if part[element] == 's':
                element, inside, inside_derivative = brackets_counter(element, inside, part)
                break
            const += part[element]

        if inside.isnumeric():
            return ans

        if inside_derivative == '1':  # если внутри нет выражения
            ans = str(f'{sign}{const}cos({inside})')
        else:
            ans = str(f'{sign}{const}cos({inside})*{inside_derivative}')

    # --------------------------------------------------------------------------------------------------------
    # проверка Косинуса

    elif lit == 'cos':
        const = ''
        inside = ''
        inside_derivative = ''

        # отдаление константы
        for element in range(len(part)):
            if part[element] == 'c':
                element, inside, inside_derivative = brackets_counter(element, inside, part)
                break
            const += part[element]

        if inside.isnumeric():
            return ans

        if inside_derivative == '1':  # если внутри нет выражения
            ans = str(f'{sign}-{const}sin({inside})')
        else:
            ans = str(f'{sign}-{const}sin({inside})*{inside_derivative}')

    # --------------------------------------------------------------------------------------------------------
    # проверка Тангенса

    elif lit == 'tan':  # 9tan(x)
        inside = inside_derivative = ''
        # опредедение константы
        if part[0].isnumeric():
            const = ''
        else:
            const = '1'
        # отдаление константы
        for element in range(0, len(part)):
            if part[element] == 't':
                element, inside, inside_derivative = brackets_counter(element, inside, part)
                break
            const += part[element]

        if inside.isnumeric():
            return ans

        if inside_derivative == '1':  # если внутри нет выражения
            ans = str(f'{sign}-{const}/cos({inside})^2')
        else:
            ans = str(f'{sign}-{const}/cos({inside})^2*{inside_derivative}')

    # --------------------------------------------------------------------------------------------------------
    # проверка Котангенса

    elif lit == 'ctg':  # 9tan(x)
        inside = inside_derivative = ''
        # опредедение константы
        if part[0].isnumeric():
            const = ''
        else:
            const = '1'
        # отдаление константы
        for element in range(0, len(part)):
            if part[element] == 'c':
                element, inside, inside_derivative = brackets_counter(element, inside, part)
                break
            const += part[element]

        if inside.isnumeric():
            return ans

        if inside_derivative == '1':  # если внутри нет выражения
            ans = str(f'{sign}{const}/sin({inside})^2')
        else:
            ans = str(f'{sign}{const}/sin({inside})^2*{inside_derivative}')

    # --------------------------------------------------------------------------------------------------------
    # проверка log

    elif lit == "log":
        arg = arg_derivative = base = ''
        # определение константы
        if part[0].isnumeric():
            const = ''
        else:
            const = '1'
        # отделение константы
        for element in range(0, len(part)):
            if part[element] == 'l':
                element += 4
                while part[element] != ']':
                    base += part[element]
                    element += 1
                element += 1
                if part[element] == '(':
                    brackets = 1
                    element += 1
                    while brackets != 0:  # part[i] != ')' and
                        if part[element] == '(':
                            brackets += 1
                        elif part[element] == ')':
                            brackets -= 1
                        if brackets != 0:
                            arg += part[element]
                        element += 1
                    if arg.isnumeric():
                        arg_derivative = 1
                    else:
                        arg_derivative = der(arg)
                    break
            const += part[element]

        if arg.isnumeric():
            return ans

        if arg_derivative == '1':  # если внутри нет выражения
            ans = str(f'{sign}({const}/{arg}*ln({base}))')
        else:
            ans = str(f'{sign}({const}*({arg_derivative})/({arg})*ln({base}))')

    # --------------------------------------------------------------------------------------------------------
    # проверка ln

    elif lit == 'ln(':
        arg = arg_derivative = ''
        # определение константы
        if part[0].isnumeric():
            const = ''
        else:
            const = '1'
        for element in range(0, len(part)):
            if part[element] == 'l':
                element += 3
                brackets = 1
                while brackets != 0:  # part[i] != ')' and
                    if part[element] == '(':
                        brackets += 1
                    elif part[element] == ')':
                        brackets -= 1
                    if brackets != 0:
                        arg += part[element]
                    element += 1
                if arg.isnumeric():
                    arg_derivative = 1
                else:
                    arg_derivative = der(arg)
                break
            const += part[element]

        if arg.isnumeric():
            return ans

        if arg_derivative == '1':  # если внутри нет выражения
            ans = str(f'{sign}({const}/{arg}')
        else:
            ans = str(f'{sign}({const}*({arg_derivative})/({arg}))')

    # --------------------------------------------------------------------------------------------------------
    # проверка exp

    elif lit == 'exp':
        arg = arg_derivative = ''
        # определение константы
        if part[0].isnumeric():
            const = ''
        else:
            const = '1'
        for element in range(0, len(part)):
            if part[element] == 'e':
                element, aeg, arg_derivative = brackets_counter(element, arg, part)
                break
            const += part[element]

        if arg.isnumeric():
            return ans

        if arg_derivative == '1':  # если внутри нет выражения
            ans = str(f'{sign}exp({arg})')
        else:
            ans = str(f'{sign}exp({arg})*({arg_derivative})')

    # --------------------------------------------------------------------------------------------------------
    # проверка x^n

    elif part.find("^") != -1:
        inside = degree = ''
        # проверка константы
        if part[0].isnumeric():
            const = ''
        else:
            const = '1'
        for element in range(0, len(part)):
            if not part[element].isnumeric():
                if pow_func(part):  # f(x)^n
                    brackets = 0
                    while True:
                        if part[element] == '(':
                            brackets += 1
                        elif part[element] == ')':
                            brackets -= 1
                        inside += part[element]
                        element += 1
                        if part[element] == '^' and brackets == 0:
                            break

                    for element_2 in range(element + 1, len(part)):
                        degree += part[element_2]

                    inside_derivative = der(inside)
                    ans = str(f'{sign}{int(const) * int(degree)}*({inside})^{int(degree) - 1}*({inside_derivative})')
                    break
                    # print(inside)

                elif part[element] == '^':  # A^x
                    for j in range(element + 1, len(part)):
                        inside += part[j]
                    inside_derivative = der(inside)
                    ans = str(f'{sign}{part}*ln({const})*({inside_derivative})')
                    break

                elif part[element] == 'x':  # x^n
                    element += 2
                    while element < len(part):
                        degree += part[element]
                        element += 1

                    ans = str(f'{sign}{int(const) * int(degree)}x^{int(degree) - 1}')
                    break
            else:
                const += part[element]

    elif part.find('x') != -1:
        ans = '1'

    return ans
