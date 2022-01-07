from Al_CCs import Al_CCs
from DAGs.DAG_base import Node
from DAG import DAG
import random
from JSONexporter import JSONexport
from Al_CCs import Method
from sys import argv

tgff_file_name = "original_20_6"
if len(argv) > 1:
    tgff_file_name = argv[1]

dag = DAG()
dag.read_file_tgff(tgff_file_name)
dag.record_pre_suc()
dag.record_src_snk()

#print([random.randint(0,10)/10 for i in range(50)])

n = [16, 8, 14, 10, 14, 15, 12, 12, 10, 9, 16, 13, 16, 13, 11, 11, 8, 15, 8, 15, 9, 12, 16, 16, 16, 14, 14, 15, 14, 10, 8, 15, 9, 9, 10, 15, 16, 16, 12, 14, 8, 8, 14, 14, 15, 8, 9, 14, 14, 10]
k = [0.8, 0.1, 1.0, 0.5, 0.0, 0.2, 0.4, 0.0, 0.7, 0.5, 0.7, 0.6, 0.1, 0.1, 0.0, 0.5, 0.4, 0.0, 0.2, 0.0, 0.4, 0.2, 0.3, 1.0, 0.3, 0.1, 0.0, 0.2, 0.8, 0.4, 0.5, 0.2, 0.9, 0.9, 0.3, 0.0, 0.0, 0.4, 0.1, 0.4, 0.0, 0.4, 0.4, 0.2, 0.2, 0.8, 0.0, 1.0, 0.6, 0.8]

dag.set_n(n)
dag.set_k(k)

dag.find_critical_path()
dag.print_critical_path()

dag.rta_fcp()

"""
nodes = []
node = Node() 
node.set(0, 320, 16, [], False) 
nodes.append(node)
node = Node() 
node.set(1, 180, 12, [0], False) 
nodes.append(node)
node = Node() 
node.set(2, 320, 16, [0], False) 
nodes.append(node)
node = Node() 
node.set(3, 160, 8, [0], False) 
nodes.append(node)
node = Node() 
node.set(4, 60, 4, [1], False) 
nodes.append(node)
node = Node() 
node.set(5, 320, 12, [2, 3], False) 
nodes.append(node)
node = Node() 
node.set(6, 160, 4, [4], False) 
nodes.append(node)
node = Node() 
node.set(7, 120, 12, [5], False) 
nodes.append(node)
node = Node() 
node.set(8, 240, 8, [6, 7], True) 
nodes.append(node)
"""
Al_CCs(dag.nodes, Method.Wait_suff)

JSONexport(dag)

for node in dag.nodes:
    print("idx: "+str(node.idx).ljust(2)+", CC: "+str(node.cc_idx)+", c: "+str(node.c).ljust(3)+", time: "+str(node.time))
# ", n: "+str(node.core_idx)+
