import string
from tkinter import *
from tkinter import ttk

import matplotlib

import sugar as sb
import matplotlib.pyplot as plt


matrix_entries = []
z_matrix = []


def on_generate_matrix_click():
    globals()['z_matrix'] = sb.gen_z_matrix(size=int(n_entry.get()),
                               min_start_sugar=float(start_sugar_from_entry.get()),
                               max_start_sugar=float(start_sugar_to_entry.get()),
                               min_degradation=float(degradation_from_entry.get()),
                               max_degradation=float(degradation_to_entry.get()),
                               min_k=float(k_from_entry.get()), max_k=float(k_from_entry.get()),
                               min_na=float(na_from_entry.get()), max_na=float(na_from_entry.get()),
                               min_an=float(an_from_entry.get()), max_an=float(an_from_entry.get()))

    show_matrix(z_matrix, 480, 100)


def show_matrix(matrix: list, x_pos, y_pos):
    x_interval = 55
    y_interval = 25

    for i in range(len(matrix_entries)):
        entry: Entry
        entry = matrix_entries[i]
        entry.destroy()

    matrix_entries.clear()

    for i in range(len(matrix)):
        str = matrix[i]
        for j in range(len(str)):
            entry = Entry(frame, width=5, font="Times 13", bg='#edf5f3')
            entry.place(x=x_pos+x_interval*j, y=y_pos+y_interval*i)
            entry.insert(0, "{0:.3f}".format(matrix[i][j]))
            matrix_entries.append(entry)


def on_run_experiments_click():
    experiments_quantity = int(experiments_quantity_entry.get())
    n = int(n_entry.get())

    hung_max_avg = []
    for i in range(n):
        hung_max_avg.append(0)

    hung_min_avg = []
    for i in range(n):
        hung_min_avg.append(0)

    greedy_avg = []
    for i in range(n):
        greedy_avg.append(0)

    saving_avg = []
    for i in range(n):
        saving_avg.append(0)

    gre_sav_avg = []
    for i in range(n):
        gre_sav_avg.append(0)

    sav_gre_avg = []
    for i in range(n):
        sav_gre_avg.append(0)

    steps = []
    for i in range(int(n)):
        steps.append(i+1)

    for k in range(experiments_quantity):
        globals()['z_matrix'] = sb.gen_z_matrix(size=int(n_entry.get()),
                                                min_start_sugar=float(start_sugar_from_entry.get()),
                                                max_start_sugar=float(start_sugar_to_entry.get()),
                                                min_degradation=float(degradation_from_entry.get()),
                                                max_degradation=float(degradation_to_entry.get()),
                                                min_k=float(k_from_entry.get()), max_k=float(k_from_entry.get()),
                                                min_na=float(na_from_entry.get()), max_na=float(na_from_entry.get()),
                                                min_an=float(an_from_entry.get()), max_an=float(an_from_entry.get()))


        values = []


        # Венгерский (max)
        value, indices = sb.hung_max(z_matrix)
        for i in range(len(indices)):
            if i == 0:
                values.append(z_matrix[indices[i]][i])
            if i != 0:
                values.append(values[i - 1] + z_matrix[indices[i]][i])
            hung_max_avg[i] += values[i]
        values.clear()

        # Венгерский (min)
        value, indices = sb.hung_min(z_matrix)
        for i in range(len(indices)):
            if i == 0:
                values.append(z_matrix[indices[i]][i])
            if i != 0:
                values.append(values[i - 1] + z_matrix[indices[i]][i])
            hung_min_avg[i] += values[i]
        values.clear()

        # Бережливый
        value, indices = sb.saving(z_matrix)
        for i in range(len(indices)):
            if i == 0:
                values.append(z_matrix[indices[i]][i])
            if i != 0:
                values.append(values[i - 1] + z_matrix[indices[i]][i])
            saving_avg[i] += values[i]
        values.clear()

        # Жадный
        value, indices = sb.greedy(z_matrix)
        for i in range(len(indices)):
            if i == 0:
                values.append(z_matrix[indices[i]][i])
            if i != 0:
                values.append(values[i - 1] + z_matrix[indices[i]][i])
            greedy_avg[i] += values[i]
        values.clear()

        # Жадно-бережливый
        value, indices = sb.greed_sav(z_matrix, len(z_matrix) / 2)
        for i in range(len(indices)):
            if i == 0:
                values.append(z_matrix[indices[i]][i])
            if i != 0:
                values.append(values[i - 1] + z_matrix[indices[i]][i])
            gre_sav_avg[i] += values[i]
        values.clear()

        # Бережливо-жадный
        value, indices = sb.sav_greed(z_matrix, len(z_matrix) / 2)
        for i in range(len(indices)):
            if i == 0:
                values.append(z_matrix[indices[i]][i])
            if i != 0:
                values.append(values[i - 1] + z_matrix[indices[i]][i])
            sav_gre_avg[i] += values[i]
        values.clear()

    for i in range(n):
        hung_max_avg[i] /= experiments_quantity
        hung_min_avg[i] /= experiments_quantity
        greedy_avg[i] /= experiments_quantity
        saving_avg[i] /= experiments_quantity
        sav_gre_avg[i] /= experiments_quantity
        gre_sav_avg[i] /= experiments_quantity


    plt.plot(steps, hung_max_avg, label="Венгерский (max)")
    plt.plot(steps, hung_min_avg, label="Венгерский (min)")
    plt.plot(steps, greedy_avg, label="Жадный")
    plt.plot(steps, saving_avg, label="Бережливый")
    plt.plot(steps, sav_gre_avg, label="Бережливо-жадный")
    plt.plot(steps, gre_sav_avg, label="Жадно-бережливый")

    plt.title("Усредненные результаты серии экспериментов")
    plt.xlabel('Этапы переработки')
    plt.ylabel('Сахара добыто')
    plt.legend()
    plt.show()


def on_run_one_experiment_click():
    steps = []
    values = []

    # Венгерский (max)
    value, indices = sb.hung_max(z_matrix)
    for i in range(len(indices)):
        steps.append(i + 1)
        if i == 0:
            values.append(z_matrix[indices[i]][i])
        if i != 0:
            values.append(values[i-1] + z_matrix[indices[i]][i])
    plt.plot(steps, values, label="Венгерский (max)")
    steps.clear()
    values.clear()

    # Венгерский (min)
    value, indices = sb.hung_min(z_matrix)
    for i in range(len(indices)):
        steps.append(i + 1)
        if i == 0:
            values.append(z_matrix[indices[i]][i])
        if i != 0:
            values.append(values[i - 1] + z_matrix[indices[i]][i])
    plt.plot(steps, values, label="Венгерский (min)")
    steps.clear()
    values.clear()

    # Бережливый
    value, indices = sb.saving(z_matrix)
    for i in range(len(indices)):
        steps.append(i + 1)
        if i == 0:
            values.append(z_matrix[indices[i]][i])
        if i != 0:
            values.append(values[i - 1] + z_matrix[indices[i]][i])
    plt.plot(steps, values, label="Бережливый")
    steps.clear()
    values.clear()

    # Жадный
    value, indices = sb.greedy(z_matrix)
    for i in range(len(indices)):
        steps.append(i + 1)
        if i == 0:
            values.append(z_matrix[indices[i]][i])
        if i != 0:
            values.append(values[i - 1] + z_matrix[indices[i]][i])
    plt.plot(steps, values, label="Жадный")
    steps.clear()
    values.clear()

    # Жадно-бережливый
    value, indices = sb.greed_sav(z_matrix, len(z_matrix) / 2)
    for i in range(len(indices)):
        steps.append(i + 1)
        if i == 0:
            values.append(z_matrix[indices[i]][i])
        if i != 0:
            values.append(values[i - 1] + z_matrix[indices[i]][i])
    plt.plot(steps, values, label="Жадно-бережливый")
    steps.clear()
    values.clear()

    # Бережливо-жадный
    value, indices = sb.sav_greed(z_matrix, len(z_matrix) / 2)
    for i in range(len(indices)):
        steps.append(i + 1)
        if i == 0:
            values.append(z_matrix[indices[i]][i])
        if i != 0:
            values.append(values[i - 1] + z_matrix[indices[i]][i])
    plt.plot(steps, values, label="Бережливо-жадный")
    steps.clear()
    values.clear()

    plt.title("Результаты одного эксперимента")
    plt.xlabel('Этапы переработки')
    plt.ylabel('Сахара добыто')
    plt.legend()
    plt.show()


root = Tk()


root['bg'] = '#fafafa'
root.geometry("1000x600")


frame = ttk.Frame()
frame.pack(fill=BOTH, expand=True, )

Label(frame, text="Количество партий:", bg='#fafafa', font="Times 13").place(x=50, y=40)
n_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
n_entry.place(x=220, y=40)

Label(frame, text="Разброс стартовой сахаристости:", bg='#fafafa', font="Times 13").place(x=50, y=70)
start_sugar_from_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
start_sugar_from_entry.place(x=300, y=70)
start_sugar_to_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
start_sugar_to_entry.place(x=350, y=70)
Label(frame, text="Разброс коэффициентов деградации:", bg='#fafafa', font="Times 13").place(x=25, y=100)
degradation_from_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
degradation_from_entry.place(x=300, y=100)
degradation_to_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
degradation_to_entry.place(x=350, y=100)



inorganic_y = 100
inorganic_x = 10

Label(frame, text="Содержание неорганики (min/max):", bg='#fafafa', font="Times 16")\
    .place(x=80+inorganic_x, y=60+inorganic_y)

Label(frame, text="Калий (ммоль/100 грамм):", bg='#fafafa', font="Times 13")\
    .place(x=85+inorganic_x, y=100+inorganic_y)
k_from_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
k_from_entry.place(x=300 + inorganic_x, y=100 + inorganic_y)
k_to_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
k_to_entry.place(x=350 + inorganic_x, y=100 + inorganic_y)


Label(frame, text="Натрий (ммоль/100 грамм):", bg='#fafafa', font="Times 13")\
    .place(x=77+inorganic_x, y=130+inorganic_y)
na_from_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
na_from_entry.place(x=300 + inorganic_x, y=130 + inorganic_y)
na_to_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
na_to_entry.place(x=350 + inorganic_x, y=130 + inorganic_y)

Label(frame, text="а-аминный азот (ммоль/100 грамм):", bg='#fafafa', font="Times 13")\
    .place(x=20+inorganic_x, y=160+inorganic_y)
an_from_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
an_from_entry.place(x=300 + inorganic_x, y=160 + inorganic_y)
an_to_entry = Entry(frame, width=5, font="Times 14", bg='#edf5f3')
an_to_entry.place(x=350 + inorganic_x, y=160 + inorganic_y)

Button(frame, text="Сгенерировать матрицу", font="Times 14", command=on_generate_matrix_click).place(x=100, y=310)

Label(frame, text="Количество экспериментов:", bg='#fafafa', font="Times 13")\
    .place(x=70, y=420)
experiments_quantity_entry = Entry(frame, width=7, font="Times 14", bg='#edf5f3')
experiments_quantity_entry.place(x=290, y=420)

Button(frame, text="Провести серию экспериментов", font="Times 14", command=on_run_experiments_click).place(x=70, y=460)

Label(frame, text="Матрица сахаристости:", bg='#fafafa', font="Times 14")\
    .place(x=500, y=35)

Button(frame, text="Провести эксперимент", font="Times 14", command=on_run_one_experiment_click).place(x=700, y=30)

matplotlib.use('TkAgg')
root.mainloop()



