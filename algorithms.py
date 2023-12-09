import numpy as np
import time as TIME
from initialization import init
from elitist_strategy import fast_non_dominated_sort
from elitist_strategy import tradition_crowd_distance
from reproduction import make_new_pop
from dismantling_models import sub_task_1



def algorithm_1(constr_mat, num_of_part, prior_constrain, disassembly_side, danger, need,
         popnum=100, crossover_prob=0.85, mutation_prob=0.25, evolution_time=100):

    start = TIME.time()
    P_t, memory_visit, memory_branch = init(num_ele=num_of_part, pop_num=popnum, temperature=1,
                                            prior_constrain=constr_mat, disassembly_side=disassembly_side)

    Q_t, memory_visit, memory_branch = make_new_pop(P_t,
                                                    crossover_prob,
                                                    mutation_prob,
                                                    num_of_part,
                                                    prior_constrain,
                                                    disassembly_side,
                                                    memory_visit,
                                                    memory_branch)

    while True:
        if TIME.time() - start >= evolution_time:
            break

        R_t = np.concatenate((P_t, Q_t))
        R_t_obj = sub_task_1(R_t, danger, need, num_of_part)

        R_t_rank, R_t_f = fast_non_dominated_sort(R_t_obj)
        R_t_crowd = tradition_crowd_distance(R_t_obj)


        elit = []
        for cut, ele in enumerate(R_t_f):
            if len(elit + ele) <= popnum:
                elit = elit + ele
            else:
                break

        candid_pop = np.array(R_t_f[cut])
        candid_pop_crowd = R_t_crowd[candid_pop]

        need_supplement_num = popnum - len(elit)
        elit = elit + candid_pop[np.argsort(candid_pop_crowd)[::-1][:need_supplement_num]].tolist()

        P_t = R_t[elit]

        Q_t, memory_visit, memory_branch = make_new_pop(P_t,
                                                        crossover_prob,
                                                        mutation_prob,
                                                        num_of_part,
                                                        prior_constrain,
                                                        disassembly_side,
                                                        memory_visit,
                                                        memory_branch)

    R_t = P_t

    R_t_obj = sub_task_1(R_t, danger, need, num_of_part)
    _, R_t_f = fast_non_dominated_sort(R_t_obj)

    return np.unique(R_t[R_t_f[0]], axis=0)