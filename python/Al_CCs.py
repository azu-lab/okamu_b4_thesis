from numpy import argmax
from numpy import argmin
from math import ceil
from DAGs.DAG_base import Node
from enum import Enum

class Method(Enum):
    Wait_suff = 0
    Al_avail = 1
    Dec_method = 2

def Al_CCs(dags: [Node], method=Method.Wait_suff):
    # initialize
    q = []
    e = [ [] for i in range(5) ]
    vacant_core = [ 16 for i in range(5) ]
    cores = [ [ i for i in range(16) ] for i in range(5) ]

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
                for i in range(v_h.n):
                    v_h.core_idx.append(cores[cc_idx].pop(0))
                e[cc_idx].append(v_h)
            else:
                if method is Method.Wait_suff:
                    q.insert(0, v_h)
                    break
                elif method is Method.Al_avail:
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
                elif method is Method.Dec_method:
                    cc_idx = argmax(vacant_core)
                    al_avail_flag = True
                    if vacant_core[cc_idx] != 0:
                        core_num = vacant_core[cc_idx]
                        tmp_time = time + v_h.sc_n(core_num)

                        for node in sorted(e[cc_idx], key=lambda u: u.time+u.sc()):
                            core_num += node.n
                            if tmp_time > node.time+node.sc()+v_h.sc_n(core_num):
                                al_avail_flag = False
                    else:
                        al_avail_flag = False

                    if al_avail_flag is True:
                        v_h.n = vacant_core[cc_idx]
                        v_h.cc_idx = cc_idx
                        v_h.time = time
                        vacant_core[cc_idx] -= v_h.n
                        e[cc_idx].append(v_h)
                    else:
                        q.insert(0, v_h)
                        break

                else:
                    print("invalid-method")
                    exit()
                

        # simulation
        # find earliest
        finish_time = 99999
        idx = (-1, -1)
        for i, ear in enumerate(e):
            for j, node in enumerate(ear):
                if node.time + node.sc() < finish_time:
                    finish_time = node.time + node.sc()
                    idx = (i, j)
        earliest = e[idx[0]].pop(idx[1])

        if earliest.snk is True:
            break
        vacant_core[idx[0]] += earliest.n
        cores[idx[0]].extend(earliest.core_idx)
        time = earliest.time + earliest.sc()
        earliest.fn_flag = True

        new_entry = []
        for dag in dags:
            flag = True
            if dag.st_flag is True:
                flag = False
            for p in dag.pre:
                if dags[p].fn_flag is not True:
                    flag = False
            if flag is True:
                dag.st_flag = True
                new_entry.append(dag)
        q.extend(sorted(new_entry, key=lambda u: u.p, reverse=True))