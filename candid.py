import copy
import numpy as np

class get_candid:
    def __init__(self, prior_constrain, disassembly_side):
        self.prior_constrain = copy.deepcopy(prior_constrain)
        self.disassembly_side = disassembly_side

    def get_can_do_task(self, did_tasks):
        did_tasks_with0_encoding = [abs(ele) - 1 for ele in did_tasks]
        self.prior_constrain[did_tasks_with0_encoding, :] = 0
        can_do_tasks = np.argwhere(np.sum(self.prior_constrain, axis=0) == 0).reshape(-1).tolist()
        for did_task in did_tasks_with0_encoding:
            can_do_tasks.remove(did_task)
        can_do_tasks = (np.array(can_do_tasks) + 1).tolist()
        can_do_tasks_duplic = copy.deepcopy(can_do_tasks)
        for ele in can_do_tasks_duplic:
            if self.disassembly_side[ele - 1] == -1:
                can_do_tasks.remove(ele)
                can_do_tasks.append(-1 * ele)
            elif self.disassembly_side[ele - 1] == 0:
                can_do_tasks.append(-1 * ele)
        return can_do_tasks