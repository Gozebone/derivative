import os
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
        inside_derivative = derivative(inside)
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

            der_1 = derivative(expressions[0])
            der_2 = derivative(expressions[1])

            return str(f'({der_1}{separator}{der_2})')

        expressions[0] += part[element]

    return part


def sign_multiply(part):
    expressions = ['', '']

    for element in range(0, len(part)):

        if part[element] == '*':

            for j in range(element + 1, len(part)):
                expressions[1] += part[j]

            der_1 = derivative(expressions[0])
            der_2 = derivative(expressions[1])

            return str(f' ({der_1} * {expressions[1]} + {expressions[0]} * {der_2})')

        expressions[0] += part[element]

    return part


def sign_div(part):
    expressions = ['', '']

    for element in range(0, len(part)):

        if part[element] == '/':

            for j in range(element + 1, len(part)):
                expressions[1] += part[j]

            der_1 = derivative(expressions[0])
            der_2 = derivative(expressions[1])

            return str(f' (( {der_1} * {expressions[1]} - {expressions[0]} * {der_2})/( {expressions[1]} )^2)')

        expressions[0] += part[element]

    return part


def derivative(part):
    ans = ''

    # проверка на внешние скобки
    while part[0] == '(' and part[len(part) - 1] == ')':
        temp = ''
        brackets = 1
        for element in range(1, len(part)-1):
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

    # проверка знака
    sign = '+'
    if part[0] == '-' or part[0] == '+':
        sign = part[0]
        # print("знак: " + sign)
        part = part[1:]

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

        if inside_derivative == '' or inside_derivative == '1':  # если внутри нет выражения
            if sign == '+':
                ans = str(f'+ {const}cos({inside})')
            elif sign == '-':
                ans = str(f'- {const}cos({inside})')
        else:
            if sign == '+':
                ans = str(f'+ {const}cos({inside}) * {inside_derivative[1:]}')
            elif sign == '-':
                ans = str(f'- {const}cos({inside}) * {inside_derivative[1:]}')

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

        if inside_derivative == '' or inside_derivative == '1':  # если внутри нет выражения
            if sign == '+':
                ans = str(f'- {const}sin({inside})')
            elif sign == '-':
                ans = str(f'+ {const}sin({inside})')
        else:
            if sign == '+':
                # ans = str(f'- {const}sin({inside}) * {inside_derivative[1:]}')
                ans = str(f'- {const}sin({inside}) * {inside_derivative}')
            elif sign == '-':
                # ans = str(f'+ {const}sin({inside}) * {inside_derivative[1:]}')
                ans = str(f'+ {const}sin({inside}) * {inside_derivative}')

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

        if inside_derivative == '' or inside_derivative == '1':  # если внутри нет выражения
            if sign == '+':
                ans = str(f'+ {const}/cos({inside})^2')
            elif sign == '-':
                ans = str(f'- {const}/cos({inside})^2')
        else:
            if sign == '+':
                ans = str(f'+ {const}/cos({inside})^2 * {inside_derivative}')
            elif sign == '-':
                ans = str(f'- {const}/cos({inside})^2 * {inside_derivative}')

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

        if inside_derivative == '' or inside_derivative == '1':  # если внутри нет выражения
            if sign == '+':
                ans = str(f'- {const}/sin({inside})^2')
            elif sign == '-':
                ans = str(f'+ {const}/sin({inside})^2')
        else:
            if sign == '+':
                ans = str(f'- {const}/sin({inside})^2 * {inside_derivative}')
            elif sign == '-':
                ans = str(f'+ {const}/sin({inside})^2 * {inside_derivative}')

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
                element += 3
                while part[element].isnumeric():
                    base += part[element]
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
                        arg_derivative = derivative(arg)
                    break
            const += part[element]

        if arg_derivative == '' or arg_derivative == '1':  # если внутри нет выражения
            if sign == '+':
                ans = str(f'+ {part}')
            elif sign == '-':
                ans = str(f'- {part}')
        else:
            if sign == '+':
                ans = str(f'+ ({const} * {arg_derivative})/(({arg}) * ln({base}))')
            elif sign == '-':
                ans = str(f'- ({const} * {arg_derivative})/(({arg}) * ln({base}))')

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
                    arg_derivative = derivative(arg)
                break
            const += part[element]
        if arg_derivative == '1':  # если внутри нет выражения
            if sign == '+':
                ans = str(f'')
            elif sign == '-':
                ans = str(f'')
        elif arg_derivative == '':
            if sign == '+':
                ans = str(f'+ {const}/{arg}')
            elif sign == '-':
                ans = str(f'- {const}/{arg}')
        else:
            if sign == '+':
                ans = str(f'+ ({const} * {arg_derivative})/{arg}')
            elif sign == '-':
                ans = str(f'- ({const} * {arg_derivative})/{arg}')

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
        if arg_derivative == '1':  # если внутри нет выражения
            if sign == '+':
                ans = str(f'')
            elif sign == '-':
                ans = str(f'')
        elif arg_derivative == '':
            if sign == '+':
                ans = str(f'+ exp({arg})')
            elif sign == '-':
                ans = str(f'- exp({arg})')
        else:
            if sign == '+':
                ans = str(f'+ exp({arg}) * {arg_derivative}')
            elif sign == '-':
                ans = str(f'- exp({arg}) * {arg_derivative}')

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
                    
                    for element_2 in range (element + 1, len(part)):
                        degree += part[element_2]

                    inside_derivative = derivative(inside)
                    ans = str(f'{int(const) * int(degree)} * ({inside}) ^ {int(degree) - 1} * ({inside_derivative})')
                    break
                    # print(inside)

                elif part[element] == '^':  # A^x
                    for j in range(element + 1, len(part)):
                        inside += part[j]
                    inside_derivative = derivative(inside)
                    ans = str(f'{part} * ln({const}) * {inside_derivative}')
                    break

                elif part[element] == 'x':  # x^n
                    element += 2
                    while element < len(part):
                        degree += part[element]
                        element += 1

                    ans = str(f'{int(const) * int(degree)}x^{int(degree) - 1}')
                    break
            else:
                const += part[element]
    return ans


# def clear(part):
#     for element in range(len(part)):



# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

# НАЧАЛО
while True:
    expression = input("Введите выражение: ")

    print(derivative(expression))
    # n = 2
    # parts = []
    #
    # # проврка скобок в начале
    # # if expression[0] == '(':
    # # brackets = True
    # # else:
    # # brackets = False
    #
    # # brackets = False
    #
    # if expression[0] == '-':
    #     first_min = True
    # else:
    #     first_min = False
    #     parts = [sing_finder(1)]
    #     print(sing_finder(1))
    #
    # for i in expression:
    #     # if i == "(":
    #     # brackets = True
    #     if i == '+' or i == '-':  # and brackets == False:
    #         parts.append(sing_finder(n))
    #         print(sing_finder(n))
    #         n += 1
    #     # elif i == ")":
    #     # brackets = False
    #
    # der_parts = ''
    # # взятие производной от каждого члена
    # for i in parts:
    #     der_parts = der_parts + derivative(str(i))
    #
    # while der_parts.find('* +') != -1:
    #     der_list = list(der_parts)
    #     der_list[der_parts.find('* +') + 1] = ''
    #     der_list[der_parts.find('* +') + 2] = ''
    #     der_parts = ''.join(der_list)
    #
    # print("Производная: " + der_parts)

    os.system("PAUSE")
    # атф и надф превращаются в энергию связей глюкозы а в последствии и другх орг соединений преобразование
    # электомагнитного солнечного излучния в энергию хим связей органиеских соединений
