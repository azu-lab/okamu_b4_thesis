import queue
from numpy import argmax
from numpy import argmin

class dag():
    def __init__(self, c, n):
        self.c = c
        self.n = n
        self.cc_idx = -1
        self.time = -1

def Al_CCs(dags: [dag]):
    # initialize
    q = queue.Queue()
    e = [ queue.Queue() for i in range(5) ]
    vacant_core = [ 16 for i in range(5) ]

    for dag in dags:
        q.put(dag)

    #while True:
        time = 0

        while q.qsize() > 0:
            v_h = q.get()
            #print([99 if i < v_h.n else i for i in vacant_core])
            cc_idx = argmin([99 if i < v_h.n else i for i in vacant_core])
            if vacant_core[cc_idx] >= v_h.n:
                v_h.cc_idx = cc_idx
                v_h.time = time
                vacant_core[cc_idx] -= v_h.n
            else:
                break