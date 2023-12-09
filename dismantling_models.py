import numpy as np


def sub_task_1(orders, danger_coef, need_coef, num_of_part):
    num_gen = orders.shape[0]
    orders = orders - 1

    coefficient = np.array(range(num_of_part)) + 1

    f1s = []
    f2s = []

    for i in range(num_gen):
        order = orders[i]
        f1s.append(sum(danger_coef[order] * coefficient))
        f2s.append(sum(need_coef[order] * coefficient))
    return np.array([f1s, f2s]).T