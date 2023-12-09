import copy
import random

import numpy as np


def get_first_position(pop, num_part, memory_visit, memory_branch):
    branch_info = []
    visit_info = []
    for i in range(num_part):
        key_chain = ''.join(str(pop_ele) for pop_ele in pop[:i+1])
        branch_info.append(memory_branch[key_chain])
        visit_info.append(memory_visit[key_chain])
    branch_visit_rate = np.array(branch_info)/(np.array(visit_info)+0.0001)
    return np.random.choice(range(num_part), p=branch_visit_rate/(np.sum(branch_visit_rate)))


def mutation(pop_, constr_mat, num_of_part, direct_constrain):
    pop_c = copy.deepcopy(pop_)
    pop_c = pop_c.tolist()
    mutation_position = np.random.randint(0, num_of_part)
    mutation_part = pop_c[mutation_position]
    pop_c.remove(mutation_part)

    if direct_constrain[np.abs(mutation_part) - 1] == 0 and np.random.uniform() < 0.5:
        mutation_part = mutation_part * -1

    predecessor_task = (np.argwhere(constr_mat[:, np.abs(mutation_part) - 1] == 1).reshape(-1) + 1).tolist()
    successor_task = (np.argwhere(constr_mat[np.abs(mutation_part) - 1, :] == 1).reshape(-1) + 1).tolist()

    if len(predecessor_task) != 0 and len(successor_task) != 0:
        for i in range(len(pop_c)):
            if np.abs(pop_c[i]) in predecessor_task:
                flagFront = i
        for i in range(len(pop_c)):
            if np.abs(pop_c[i]) in successor_task:
                flagBack = i
                break
        pop_c.insert(np.random.choice(range(flagFront + 1, flagBack + 1)), mutation_part)

    elif len(predecessor_task) != 0:
        for i in range(len(pop_c)):
            if np.abs(pop_c[i]) in predecessor_task:
                flagFront = i
        pop_c.insert(np.random.choice(range(flagFront + 1, len(pop_c) + 1)), mutation_part)

    elif len(successor_task) != 0:
        for i in range(len(pop_c)):
            if np.abs(pop_c[i]) in successor_task:
                flagBack = i
                break
        pop_c.insert(np.random.choice(range(0, flagBack + 1)), mutation_part)

    else:
        pop_c.insert(np.random.choice(range(0, len(pop_c))), mutation_part)

    pop_c = np.array(pop_c)
    return pop_c


def crossover(pop1, pop2, num_of_part, memory_visit, memory_branch):
    pop_a = copy.deepcopy(pop1)
    pop_b = copy.deepcopy(pop2)

    start = get_first_position(pop_a, num_of_part, memory_visit, memory_branch)
    end = np.random.choice(range(start, num_of_part))

    piece = []
    for i in range(num_of_part):
        if pop_b[i] in pop_a[start:end + 1] or -1 * pop_b[i] in pop_a[start:end + 1]:
            piece.append(pop_b[i])
    pop_a[start:end + 1] = piece
    return pop_a


def make_new_pop(P_, crossover_prob,
                 mutation_prob, num_part, constr_mat, direct_constrain, memory_visit, memory_branch):

    P = copy.deepcopy(P_)

    popnum = len(P)
    Q = []

    for _ in range(int(popnum / 2)):
        i = random.randint(0, popnum - 1)
        j = random.randint(0, popnum - 1)
        while i == j:
            j = random.randint(0, popnum - 1)
        parent1 = P[i]
        parent2 = P[j]

        cross_mutation_offspring_1 = parent1
        cross_mutation_offspring_2 = parent2
        if np.random.uniform() < crossover_prob:
            cross_mutation_offspring_1 = crossover(parent1, parent2, num_part, memory_visit, memory_branch)
            cross_mutation_offspring_2 = crossover(parent2, parent1, num_part, memory_visit, memory_branch)
        if np.random.uniform() < mutation_prob:
            cross_mutation_offspring_1 = mutation(cross_mutation_offspring_1,
                                                  constr_mat, num_part, direct_constrain)
            cross_mutation_offspring_2 = mutation(cross_mutation_offspring_2,
                                                  constr_mat, num_part, direct_constrain)

        Q.append(cross_mutation_offspring_1.tolist())
        Q.append(cross_mutation_offspring_2.tolist())

        for offspring_index in range(num_part):
            key_offspring_1_chain = cross_mutation_offspring_1[:offspring_index + 1]
            key_offspring_2_chain = cross_mutation_offspring_2[:offspring_index + 1]
            visit_dic_key_1 = ''.join(str(pop_ele) for pop_ele in key_offspring_1_chain)
            visit_dic_key_2 = ''.join(str(pop_ele) for pop_ele in key_offspring_2_chain)

            if offspring_index == num_part - 1:
                if memory_visit.get(visit_dic_key_1) == None and memory_visit.get(visit_dic_key_2) != None:
                    for sub_offspring_index in range(num_part):
                        key_offspring_1_chain = cross_mutation_offspring_1[:sub_offspring_index + 1]
                        branch_dic_key_1 = ''.join(str(pop_ele) for pop_ele in key_offspring_1_chain)
                        if memory_branch.get(branch_dic_key_1) != None:
                            memory_branch[branch_dic_key_1] += 1
                        else:
                            memory_branch[branch_dic_key_1] = 1
                elif memory_visit.get(visit_dic_key_1) != None and memory_visit.get(visit_dic_key_2) == None:
                    for sub_offspring_index in range(num_part):
                        key_offspring_2_chain = cross_mutation_offspring_2[:sub_offspring_index + 1]
                        branch_dic_key_2 = ''.join(str(pop_ele) for pop_ele in key_offspring_2_chain)
                        if memory_branch.get(branch_dic_key_2) != None:
                            memory_branch[branch_dic_key_2] += 1
                        else:
                            memory_branch[branch_dic_key_2] = 1

                elif memory_visit.get(visit_dic_key_1) == None and memory_visit.get(visit_dic_key_2) == None:
                    if np.all(cross_mutation_offspring_1 == cross_mutation_offspring_2):
                        for sub_offspring_index in range(num_part):
                            key_offspring_1_chain = cross_mutation_offspring_1[:sub_offspring_index + 1]
                            branch_dic_key_1 = ''.join(str(pop_ele) for pop_ele in key_offspring_1_chain)
                            if memory_branch.get(branch_dic_key_1) != None:
                                memory_branch[branch_dic_key_1] += 1
                            else:
                                memory_branch[branch_dic_key_1] = 1
                    else:
                        for sub_offspring_index in range(num_part):
                            key_offspring_1_chain = cross_mutation_offspring_1[:sub_offspring_index + 1]
                            branch_dic_key_1 = ''.join(str(pop_ele) for pop_ele in key_offspring_1_chain)
                            if memory_branch.get(branch_dic_key_1) != None:
                                memory_branch[branch_dic_key_1] += 1
                            else:
                                memory_branch[branch_dic_key_1] = 1
                        for sub_offspring_index in range(num_part):
                            key_offspring_2_chain = cross_mutation_offspring_2[:sub_offspring_index + 1]
                            branch_dic_key_2 = ''.join(str(pop_ele) for pop_ele in key_offspring_2_chain)
                            if memory_branch.get(branch_dic_key_2) != None:
                                memory_branch[branch_dic_key_2] += 1
                            else:
                                memory_branch[branch_dic_key_2] = 1
            if memory_visit.get(visit_dic_key_1) != None:
                memory_visit[visit_dic_key_1] += 1
            else:
                memory_visit[visit_dic_key_1] = 1

            if memory_visit.get(visit_dic_key_2) != None:
                memory_visit[visit_dic_key_2] += 1
            else:
                memory_visit[visit_dic_key_2] = 1

    return np.array(Q), memory_visit, memory_branch