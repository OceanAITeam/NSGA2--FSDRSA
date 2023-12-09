from dismantling_models import sub_task_1
def get_scheme_perform(seqs, data_info, danger, need, num_of_part):
    schemes = []
    for seq in seqs:
        sub_scheme = []
        for task_id in seq - 1:
            sub_scheme.append(data_info[task_id][1])
        schemes.append(sub_scheme)
    return schemes, sub_task_1(seqs, danger, need, num_of_part)