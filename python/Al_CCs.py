from numpy import argmax
from numpy import argmin
from math import ceil
from DAGs.DAG_base import Node

def Al_CCs(dags: [Node], method="Wait-suff"):
    # initialize
    q = []
    e = [ [] for i in range(5) ]
    vacant_core = [ 16 for i in range(5) ]

    time = 0

    dags[0].time = 0
    dags[0].st_flag = True
    q.append(dags[0])

    while True:
        
        # allocation
        while len(q) > 0:
            v_h = q.pop(0)
            #print([99 if i < v_h.n else i for i in vacant_core])
            cc_idx = argmin([99 if i < v_h.n else i for i in vacant_core])
            if vacant_core[cc_idx] >= v_h.n:
                v_h.cc_idx = cc_idx
                v_h.time = time
                vacant_core[cc_idx] -= v_h.n
                e[cc_idx].append(v_h)
            else:
                if method == "Wait-suff":
                    q.insert(0, v_h)
                    break
                elif method == "Al-avail":
                    cc_idx = argmax(vacant_core)
                    if vacant_core[cc_idx] != 0:
                        v_h.n = vacant_core[cc_idx]
                        v_h.cc_idx = cc_idx
                        v_h.time = time
                        vacant_core[cc_idx] -= v_h.n
                        e[cc_idx].append(v_h)
                    else:
                        q.insert(0, v_h)
                        break
                # Dec-method
                else:
                    print("invalid-method")
                    exit()
                

        # simulation
        # find earliest
        finish_time = 99999
        idx = (-1, -1)
        for i, ear in enumerate(e):
            for j, node in enumerate(ear):
                if node.time + ceil(node.c / node.n) < finish_time:
                    finish_time = node.time + ceil(node.c / node.n)
                    idx = (i, j)
        earliest = e[idx[0]].pop(idx[1])

        if earliest.snk is True:
            break
        vacant_core[idx[0]] += earliest.n
        time = earliest.time + ceil(earliest.c / earliest.n)
        earliest.fn_flag = True

        for dag in dags:
            flag = True
            if dag.st_flag is True:
                flag = False
            for p in dag.pre:
                if dags[p].fn_flag is not True:
                    flag = False
            if flag is True:
                dag.st_flag = True
                q.append(dag)