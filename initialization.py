import numpy as np
from candid import get_candid
from choice_prob import getChoiceProb


def init(num_ele, pop_num, temperature, prior_constrain, disassembly_side):
    memory_visit = dict()
    memory_branch = dict()
    pops = []

    while len(pops) < pop_num:
        pop = []
        candidate = get_candid(prior_constrain, disassembly_side)
        candid_nodes = candidate.get_can_do_task(pop)
        candid_nodes = (np.array(candid_nodes) + num_ele).tolist()

        while len(pop) < num_ele:
            layer = len(pop)
            if layer == 0:
                candid_chain = [pop + [ele - num_ele] for ele in candid_nodes]

                condid_brance_info = []
                condid_visit_info = []
                for candid_chain_ele in candid_chain:
                    candid_dic_key = ''.join(str(candid_chain_ele_ele)
                                             for candid_chain_ele_ele in candid_chain_ele)
                    if memory_branch.get(candid_dic_key) != None:
                        condid_brance_info.append(memory_branch[candid_dic_key])
                    else:
                        condid_brance_info.append(0)

                    if memory_visit.get(candid_dic_key) != None:
                        condid_visit_info.append(memory_visit[candid_dic_key])
                    else:
                        condid_visit_info.append(0)
                condid_brance_info = np.array(condid_brance_info)
                condid_visit_info = np.array(condid_visit_info)

                parent_visit_info = []
                for candid_nodes_ele in candid_nodes:
                    parent_dic_key = str(candid_nodes_ele - num_ele)
                    if memory_visit.get(parent_dic_key) != None:
                        parent_visit_info.append(memory_visit[parent_dic_key])
                    else:
                        parent_visit_info.append(0)
                parent_visit_info = np.sum(parent_visit_info)

                choice_prob = getChoiceProb(condid_brance_info, condid_visit_info, parent_visit_info,
                                            temperature, 1 - len(pops) / pop_num)
                choiced_node = np.random.choice(candid_nodes, p=choice_prob)

                pop.append(choiced_node - num_ele)


            else:
                candid_chain = [pop + [ele - num_ele] for ele in candid_nodes]

                condid_brance_info = []
                condid_visit_info = []
                for candid_chain_ele in candid_chain:
                    candid_dic_key = ''.join(str(candid_chain_ele_ele)
                                             for candid_chain_ele_ele in candid_chain_ele)
                    if memory_branch.get(candid_dic_key) != None:
                        condid_brance_info.append(memory_branch[candid_dic_key])
                    else:
                        condid_brance_info.append(0)

                    if memory_visit.get(candid_dic_key) != None:
                        condid_visit_info.append(memory_visit[candid_dic_key])
                    else:
                        condid_visit_info.append(0)
                condid_brance_info = np.array(condid_brance_info)
                condid_visit_info = np.array(condid_visit_info)

                parent_dic_key = ''.join(str(pop_ele) for pop_ele in pop)
                parent_visit_info = memory_visit[parent_dic_key]

                choice_prob = getChoiceProb(condid_brance_info, condid_visit_info, parent_visit_info,
                                            temperature, 1 - len(pops) / pop_num)
                choiced_node = np.random.choice(candid_nodes, p=choice_prob)

                pop.append(choiced_node - num_ele)

            dic_key = ''.join(str(pop_ele) for pop_ele in pop)
            if memory_visit.get(dic_key) != None:
                memory_visit[dic_key] += 1
            else:
                memory_visit[dic_key] = 1

            candid_nodes = candidate.get_can_do_task(pop)
            flag = 0
            candid_nodes = (np.array(candid_nodes) + num_ele).tolist()
        pops.append(pop)

        if memory_visit.get(dic_key) == 1:
            for index_unique_pop in range(len(pop)):
                branch_key = ''.join(str(unique_pop_ele) for unique_pop_ele in pop[:index_unique_pop + 1])
                if memory_branch.get(branch_key) != None:
                    memory_branch[branch_key] += 1
                else:
                    memory_branch[branch_key] = 1
    return np.array(pops), memory_visit, memory_branch