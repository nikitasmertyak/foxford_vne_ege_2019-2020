from math import *

def root_newton(f, f_derivative, x: float, epsilon: float):
    """ Поиск корня методом Ньютона.
        f(x) - функция, для которой ищется корень f(x) =0.
        f_derivative(x) - производная этой функции.
        epsilon - требуемая погрешность нахождения корня.
    """
    iterations_counter = 1
    old_x = x
    x = x - f(x) / f_derivative(x)
    while abs(x - old_x) > epsilon:
        old_x = x
        x = x - f(x) / f_derivative(x)
        iterations_counter += 1
    print("DEBUG: сошёлся за", iterations_counter, "итераций.")
    return x
        
def f(x):
    return sin(x) - x / 2

def f_derivative(x):
    return cos(x) - 1 / 2
    
root = root_newton(f, f_derivative, 3.0, 1e-15)
print("Корень:", root)
