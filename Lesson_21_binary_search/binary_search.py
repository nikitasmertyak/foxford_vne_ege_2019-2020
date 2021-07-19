from math import *

def root_binary_search(f, a: float, b: float, epsilon: float):
    """
    Поиск корня методом половинного деления
    f - непрерывная на [a, b] функция, при этом f(a) * f(b) < 0
    epsilon - требуемая погрешность нахождения корня
    """
    assert f(a) * f(b) < 0, "Не знакопеременная функция"
    while (b - a) / 2 > epsilon:
        c = (a + b) / 2
        if f(a) * f(c) < 0:
            b = c
        elif f(c) * f(b) < 0:
            a = c
        else: # f(c) == 0
            return c
    return (a + b) / 2

def f1(x):
    return sin(x) - x / 2

print(root_binary_search(f1, 0.2, 3.0, 1e-15))
