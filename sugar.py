import random
import utility as ut
import numpy
from scipy.optimize import linear_sum_assignment


def gen_z_matrix(size: int, min_start_sugar: float, max_start_sugar: float,
                 min_degradation: float, max_degradation: float,
                 min_k: float, max_k: float,
                 min_na: float, max_na: float,
                 min_an: float, max_an: float):
    """Возвращает матрицу Z для решения задачи оптимизации, используя заданные интервалы разброса начальных условий.\n
    size - размер матрицы P\n
    min_start_sugar, max_start_sugar - интервал разброса стартовых значений сахаристости (должны быть от 0 до 1!)\n
    min_degradation, max_degradation - коэффициенты деградации будут от min_degradation до max_degradation (должны быть от 0 до 1!)\n
    min_k, max_k - минимальное и максимальное количество калия в ммоль на 100 грамм,
    min_na, max_na - минимальное и максимальное количество натрия в ммоль на 100 грамм,
    min_an, max_an - минимальное и максимальное количество а-аминного азота в ммоль на 100 грамм,"""

    k_list = []
    for i in range(size):
        k_list.append(random.uniform(min_k, max_k))

    na_list = []
    for i in range(size):
        na_list.append(random.uniform(min_na, max_na))

    an_list = []
    for i in range(size):
        an_list.append(random.uniform(min_an, max_an))

    a_vector = ut.create_vector(size, min_start_sugar, max_start_sugar)
    b_matrix = ut.create_matrix(size, size - 1, min_degradation, max_degradation)
    p_matrix = ut.create_p_matrix(a_vector, b_matrix)
    z_matrix = ut.create_z_matrix(p_matrix, k_list, na_list, an_list)
    return z_matrix


def hung_min(z_matrix):
    """Возвращает результат и список-перестановку целевой функции, поиск худшего результата с помощью венгерского алгоритма."""
    row_indices, col_indices = linear_sum_assignment(z_matrix)
    result = 0
    for i in range(len(row_indices)):
        result += z_matrix[row_indices[i]][col_indices[i]]

    for i in range(len(row_indices)):
        row_indices[col_indices[i]] = i
    return result, row_indices


def hung_max(z_matrix):
    """Возвращает результат и список-перестановку целевой функции, поиск лучшего результата с помощью венгерского алгоритма."""
    max_elem = numpy.max(z_matrix)
    reverse_p_matrix = numpy.copy(z_matrix)
    for i in range(len(z_matrix)):
        for j in range(len(z_matrix)):
            reverse_p_matrix[i][j] = -1 * z_matrix[i][j] + max_elem

    row_indices, col_indices = linear_sum_assignment(reverse_p_matrix)
    result = 0
    for i in range(len(row_indices)):
        result += z_matrix[row_indices[i]][col_indices[i]]

    for i in range(len(row_indices)):
        row_indices[col_indices[i]] = i
    return result, row_indices


def greedy(z_matrix: list):
    """Возвращает результат и список-перестановку целевой функции, поиск результата с помощью жадного алгоритма."""
    result = 0
    indices = []
    took = []

    for j in range(len(z_matrix)):
        col_max = 0
        col_max_index: int
        for i in range(len(z_matrix)):
            is_took = False

            for k in range(len(took)):
                if took[k] == i:
                    is_took = True
                    break

            if is_took:
                continue

            if z_matrix[i][j] > col_max:
                col_max = z_matrix[i][j]
                col_max_index = i
        result += col_max
        indices.append(col_max_index)
        took.append(col_max_index)
    return result, indices


def saving(z_matrix: list):
    """Возвращает результат и список-перестановку целевой функции, поиск результата с помощью бережливого алгоритма."""
    result = 0
    indices = []
    took = []

    for j in range(len(z_matrix)):
        col_min = 10000000
        col_min_index: int
        for i in range(len(z_matrix)):
            is_took = False

            for k in range(len(took)):
                if took[k] == i:
                    is_took = True
                    break

            if is_took:
                continue

            if z_matrix[i][j] < col_min:
                col_min = z_matrix[i][j]
                col_min_index = i
        result += col_min
        indices.append(col_min_index)
        took.append(col_min_index)
    return result, indices


def sav_greed(z_matrix: list, saving_steps: int):
    """Возвращает результат и список-перестановку целевой функции, поиск результата с помощью бережливо-жадного алгоритма.\n
    saving_steps - количество шагов в режиме сбережения, далее будет жадный режим."""
    result = 0
    indices = []
    took = []
    saving_steps_completed = 0

    for j in range(len(z_matrix)):

        col_min = 10000000
        col_min_index: int

        col_max = 0
        col_max_index: int

        saving_mode = saving_steps_completed < saving_steps

        for i in range(len(z_matrix)):
            is_took = False

            for k in range(len(took)):
                if took[k] == i:
                    is_took = True
                    break

            if is_took:
                continue

            if saving_mode and z_matrix[i][j] < col_min:
                col_min = z_matrix[i][j]
                col_min_index = i

            if not saving_mode and z_matrix[i][j] > col_max:
                col_max = z_matrix[i][j]
                col_max_index = i

        if saving_mode:
            result += col_min
            indices.append(col_min_index)
            took.append(col_min_index)

        else:
            result += col_max
            indices.append(col_max_index)
            took.append(col_max_index)

        saving_steps_completed += 1

    return result, indices


def greed_sav(z_matrix: list, greedy_steps: int):
    """Возвращает результат и список-перестановку целевой функции, поиск результата с помощью жадно-бережливого алгоритма.\n
    greedy_steps - количество шагов в режиме жадности, далее будет бережливый режим."""
    result = 0
    indices = []
    took = []
    greedy_steps_completed = 0

    for j in range(len(z_matrix)):

        col_min = 1000000
        col_min_index: int

        col_max = 0
        col_max_index: int

        greedy_mode = greedy_steps_completed < greedy_steps

        for i in range(len(z_matrix)):
            is_took = False

            for k in range(len(took)):
                if took[k] == i:
                    is_took = True
                    break

            if is_took:
                continue

            if not greedy_mode and z_matrix[i][j] < col_min:
                col_min = z_matrix[i][j]
                col_min_index = i

            if greedy_mode and z_matrix[i][j] > col_max:
                col_max = z_matrix[i][j]
                col_max_index = i

        if greedy_mode:
            result += col_max
            indices.append(col_max_index)
            took.append(col_max_index)

        else:
            result += col_min
            indices.append(col_min_index)
            took.append(col_min_index)

        greedy_steps_completed += 1

    return result, indices



