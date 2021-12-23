from Al_CCs import Al_CCs
from DAGs.DAG_base import Node
from DAGs.DAG_TGFF_load import DAG_TGFF
import random

dag = DAG_TGFF("original_20_6")
dag.read_file_tgff()
dag.record_pre_suc()
dag.record_src_snk()

#print([random.randint(8, 16) for i in range(50)])

n = [16, 8, 14, 10, 14, 15, 12, 12, 10, 9, 16, 13, 16, 13, 11, 11, 8, 15, 8, 15, 9, 12, 16, 16, 16, 14, 14, 15, 14, 10, 8, 15, 9, 9, 10, 15, 16, 16, 12, 14, 8, 8, 14, 14, 15, 8, 9, 14, 14, 10]

dag.set_n(n)

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
Al_CCs(dag.nodes, "Al-avail")

for node in dag.nodes:
    print("idx: "+str(node.idx)+", CC: "+str(node.cc_idx)+", n: "+str(node.n)+", c: "+str(node.c)+", time: "+str(node.time))
