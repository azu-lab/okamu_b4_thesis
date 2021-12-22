from Al_CCs import Al_CCs
from Al_CCs import dag
from DAGs.DAG_base import Node

dags = []
dag = Node() 
dag.set(0, 320, 16, [], False) 
dags.append(dag)
dag = Node() 
dag.set(1, 180, 12, [0], False) 
dags.append(dag)
dag = Node() 
dag.set(2, 320, 16, [0], False) 
dags.append(dag)
dag = Node() 
dag.set(3, 160, 8, [0], False) 
dags.append(dag)
dag = Node() 
dag.set(4, 60, 4, [1], False) 
dags.append(dag)
dag = Node() 
dag.set(5, 320, 12, [2, 3], False) 
dags.append(dag)
dag = Node() 
dag.set(6, 160, 4, [4], False) 
dags.append(dag)
dag = Node() 
dag.set(7, 120, 12, [5], False) 
dags.append(dag)
dag = Node() 
dag.set(8, 240, 8, [6, 7], True) 
dags.append(dag)

Al_CCs(dags)

for dag in dags:
    print("idx: "+str(dag.idx)+", CC: "+str(dag.cc_idx)+", time: "+str(dag.time))