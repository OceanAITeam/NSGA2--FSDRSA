import numpy as np


def compare(p1, p2):
    D = len(p1)
    p1_dominate_p2 = True
    p2_dominate_p1 = True
    for i in range(D):
        if p1[i] > p2[i]:
            p1_dominate_p2 = False
        if p1[i] < p2[i]:
            p2_dominate_p1 = False

    if p1_dominate_p2 == p2_dominate_p1:
        return 0
    return 1 if p1_dominate_p2 else -1

def fast_non_dominated_sort(P):
    P_size = len(P)
    n = np.full(shape=P_size, fill_value=0)
    S = []
    f = []
    rank = np.full(shape=P_size, fill_value=-1)
    f_0 = []
    for p in range(P_size):
        n_p = 0
        S_p = []
        for q in range(P_size):
            if p == q:
                continue
            cmp = compare(P[p], P[q])
            if cmp == 1:
                S_p.append(q)
            elif cmp == -1:
                n_p += 1
        S.append(S_p)
        n[p] = n_p
        if n_p == 0:
            rank[p] = 0
            f_0.append(p)
    f.append(f_0)
    i = 0
    while len(f[i]) != 0:
        Q = []
        for p in f[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    rank[q] = i + 1
                    Q.append(q)
        i += 1
        f.append(Q)
    rank +=1
    return rank,f

def tradition_crowd_distance(popf):
    I = popf.shape[0]
    popDistance = np.zeros(shape=(I))
    for M in range(popf.shape[1]):
        popIndex = np.argsort(popf[:,M])
        popDistance[popIndex[0]] = 9999999999999999999999
        popDistance[popIndex[-1]] = 9999999999999999999999
        for i in range(1, I-1):
            popDistance[popIndex[i]] = popDistance[popIndex[i]] + (popf[:,M][popIndex[i+1]] - popf[:,M][popIndex[i-1]])/(popf[:,M][popIndex[-1]] - popf[:,M][popIndex[0]] + 0.000000001)
    return popDistance