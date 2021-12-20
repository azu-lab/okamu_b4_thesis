from Al_CCs import Al_CCs
from Al_CCs import dag

snk = dag(256, 8)
snk.snk = True
dags = [dag(32,16), dag(18,12), dag(32,16), dag(16,8), dag(6,4), dag(32,12), dag(16,4), dag(12,12), snk]

Al_CCs(dags)

for dag in dags:
    print("CC: "+str(dag.cc_idx)+", time: "+str(dag.time))