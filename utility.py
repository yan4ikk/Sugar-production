
from random import uniform
# Отсюда ничего брать не надо, все нужные функции находятся в sugar.py

def create_vector(n: int, _min: float, _max: float):
    """Возвращает список размера n со случайными значениями от _min до _max."""
    result = []
    for i in range(n):
        result.append(uniform(_min, _max))
    return result


def create_matrix(_str: int, _col: int, _min: float, _max: float):
    """Возвращает двумерный список размера (_str)x(_col) со случайными значениями от _min до _max."""
    result = []
    for i in range(_str):
        _str = []
        for j in range(_col):
            _str.append(uniform(_min, _max))
        result.append(_str)
    return result


def create_p_matrix(a_vector, b_matrix):
    """Возвращает матрицу P для решения задачи оптимизации (Элементы в ней не могут быть больше 1)."""
    result = []
    n = len(a_vector)

    for i in range(n):
        _str = [a_vector[i]]
        for j in range(1, n):
            res = _str[j - 1] * b_matrix[i][j - 1]
            if res > 1:
                res = 1
            _str.append(res)
        result.append(_str)
    return result


def create_z_matrix(p_matrix, k_list: list, na_list: list, an_list: list):
    """Возвращает матрицу Z для решения задачи оптимизации с учетом неорганики\n
     (Элементы в ней не могут быть больше 1).\n
     k_list - список содержания калия в свекле (ммоль на 100 г свеклы)
     na_list - список содержания натрия в свекле (ммоль на 100 г свеклы)
     an_list - список содержания а-аминного азота в свекле (ммоль на 100 г свеклы)"""
    z_matrix = p_matrix
    n = len(z_matrix)

    for i in range(n):
        inorganic_effect = 0.01 * (2.1 + 0.0498 * k_list[i] + 0.878 * na_list[i] + 0.2345 * an_list[i] + 1.407)
        for j in range(n):
            z_matrix[i][j] -= inorganic_effect
            if z_matrix[i][j] < 0:
                z_matrix[i][j] = 0

    return z_matrix
