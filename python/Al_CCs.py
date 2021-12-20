from numpy import argmax
from numpy import argmin

class dag():
    def __init__(self, c, n):
        self.c = c
        self.n = n
        self.cc_idx = -1
        self.time = -1
        self.snk = False

def Al_CCs(dags: [dag]):
    # initialize
    q = []
    e = [ [] for i in range(5) ]
    vacant_core = [ 16 for i in range(5) ]

    q.extend(dags)

    time = 0
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
                q.insert(0, v_h)
                break

        # simulation
        # find earliest
        finish_time = 99999
        idx = (-1, -1)
        for i, ear in enumerate(e):
            for j, node in enumerate(ear):
                if node.time + node.c < finish_time:
                    finish_time = node.time + node.c
                    idx = (i, j)
        earliest = e[idx[0]].pop(idx[1])

        if earliest.snk is True:
            break
        vacant_core[idx[0]] += earliest.n
        time = earliest.c
        