import sugar as sb

# Пример
# Вводим стартовые значения и интервалы - получаем матрицу P
z = sb.gen_z_matrix(size=5,
                    min_start_sugar=0.8, max_start_sugar=1,
                    min_degradation=0.7, max_degradation=0.9,
                    min_k=4, max_k=6,
                    min_na=2, max_na=4,
                    min_an=2, max_an=5)

# Вывод матрицы P
for i in range(len(z)):
    print(z[i])

# Используем сгенерированную матрицу P и передаем ее в функции расчета


# Венгерский минимальный
res, indices = sb.hung_min(z)
print("hungarian_min")
print(res)
print(indices)

# Венгерский максимальный
res, indices = sb.hung_max(z)
print("hungarian_max")
print(res)
print(indices)

# Жадный алгоритм
res, indices = sb.greedy(z)
print("greedy")
print(res)
print(indices)

# Бережливый алгоритм
res, indices = sb.saving(z)
print("saving")
print(res)
print(indices)

# Бережливо-жадный алгоритм
res, indices = sb.sav_greed(z, 1)
print("saving_greedy")
print(res)
print(indices)

# Жадно-бережливый алгоритм
res, indices = sb.greed_sav(z, 1)
print("greedy_saving")
print(res)
print(indices)






