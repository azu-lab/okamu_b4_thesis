from Al_CCs import Al_CCs
from Al_CCs import dag

dags = [dag(32,16), dag(18,12), dag(32,16), dag(16,8), dag(8,8)]

Al_CCs(dags)

for dag in dags:
    print("CC: "+str(dag.cc_idx)+", time: "+str(dag.time))