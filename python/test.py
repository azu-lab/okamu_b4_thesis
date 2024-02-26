from .proposed_method import WaitSufficient, AllocateAvailable, DecisionMethod, Basic
from .DAGs.DAG_base import Node
from .DAG_Constructer import DAG_Constructer
import sys
from .evaluate.JSONexporter import JSONexport
import time

def work_load(nodes: list[Node]):
    makespan = 0
    for node in nodes:
        makespan += node.c

    for node in nodes:
        if node.snk is True:
            node.start_time = makespan
            node.start_time -= node.amdahl_exec_time()

def test(file_name: str, method: str, n: list[int] | None = None, k_param: float | None = None):

    # start = time.perf_counter()

    dag = DAG_Constructer.create_dag_from_tgff_file(file_name)

    # n = 1-16 default
    if n is None:
        n = [9, 8, 11, 14, 15, 3, 16, 12, 14, 14, 16, 7, 12, 7, 7, 5, 9, 10, 13, 15, 6, 8, 9, 2, 12, 10, 16, 16, 4, 8, 2, 12, 2, 7, 8, 1, 1, 10, 11, 16, 8, 3, 2, 1, 1, 14, 6, 1, 4, 9, 9, 7, 10, 4, 8, 8, 11, 16, 6, 16, 7, 6, 6, 7, 8, 2, 2, 13, 2, 3, 4, 4, 16, 15, 7, 15, 1, 3, 7, 3, 9, 6, 10, 15, 11, 8, 14, 12, 7, 8, 13, 4, 12, 3, 15, 6, 16, 14, 12, 12, 8, 1, 16, 6, 6, 12, 1, 5, 6, 1, 9, 8, 9, 5, 11, 13, 12, 4, 13, 9, 9, 14, 13, 14, 7, 11, 1, 16, 16, 5, 8, 8, 2, 15, 3, 10, 16, 16, 12, 2, 2, 10, 7, 9, 5, 14, 1, 3, 3, 7, 7, 1, 7, 4, 9, 2, 9, 11, 3, 11, 10, 9, 2, 2, 6, 16, 5, 2, 11, 16, 5, 2, 9, 1, 9, 2, 3, 10, 6, 5, 6, 9, 16, 14, 15, 3, 14, 4, 4, 11, 6, 8, 14, 16, 2, 2, 13, 15, 15, 11, 1, 15, 11, 1, 3, 3, 9, 16, 7, 9, 14, 1, 1, 7, 7, 16, 15, 8, 14, 12, 5, 2, 5, 3, 3, 7, 3, 9, 8, 8, 16, 4, 2, 14, 8, 12, 7, 14, 6, 16, 14, 10, 9, 16, 11, 7, 7, 12, 9, 7, 7, 7, 9, 15, 13, 3, 3, 14, 7, 4, 14, 15, 12, 1, 2, 10, 11, 8, 11, 7, 10, 16, 15, 14, 10, 9, 14, 16, 1, 16, 6, 11, 4, 4, 11, 8, 4, 9, 15, 15, 3, 11, 13, 11, 3, 3, 9, 11, 3, 4]
    if method != 'rta-cpf-eo':
        dag.set_n(n)

    # k = [0.3, 0.9] default
    # print([random.randint(3,9)/10 for i in range(300)])
    if k_param is None:
        k = [0.4, 0.7, 0.8, 0.9, 0.6, 0.4, 0.7, 0.9, 0.3, 0.4, 0.9, 0.7, 0.7, 0.9, 0.8, 0.6, 0.8, 0.5, 0.3, 0.3, 0.9, 0.4, 0.4, 0.9, 0.4, 0.4, 0.9, 0.8, 0.8, 0.3, 0.4, 0.9, 0.4, 0.4, 0.9, 0.8, 0.6, 0.8, 0.6, 0.4, 0.8, 0.3, 0.4, 0.6, 0.5, 0.4, 0.5, 0.9, 0.7, 0.7, 0.9, 0.8, 0.3, 0.4, 0.6, 0.5, 0.6, 0.3, 0.6, 0.9, 0.8, 0.5, 0.3, 0.8, 0.9, 0.8, 0.6, 0.6, 0.5, 0.6, 0.8, 0.5, 0.3, 0.8, 0.8, 0.5, 0.7, 0.6, 0.7, 0.9, 0.3, 0.8, 0.8, 0.3, 0.8, 0.5, 0.5, 0.9, 0.3, 0.5, 0.8, 0.8, 0.6, 0.7, 0.8, 0.6, 0.5, 0.6, 0.8, 0.6, 0.5, 0.6, 0.4, 0.5, 0.6, 0.3, 0.7, 0.7, 0.6, 0.3, 0.3, 0.5, 0.5, 0.3, 0.4, 0.8, 0.5, 0.4, 0.4, 0.8, 0.7, 0.5, 0.9, 0.7, 0.3, 0.7, 0.8, 0.9, 0.5, 0.3, 0.5, 0.5, 0.9, 0.3, 0.9, 0.6, 0.8, 0.8, 0.6, 0.6, 0.6, 0.3, 0.9, 0.3, 0.8, 0.9, 0.4, 0.8, 0.9, 0.8, 0.9, 0.6, 0.5, 0.9, 0.7, 0.3, 0.6, 0.4, 0.8, 0.4, 0.9, 0.6, 0.4, 0.4, 0.9, 0.7, 0.9, 0.4, 0.3, 0.8, 0.9, 0.3, 0.8, 0.9, 0.5, 0.6, 0.4, 0.6, 0.9, 0.8, 0.4, 0.3, 0.7, 0.9, 0.8, 0.8, 0.7, 0.7, 0.4, 0.8, 0.7, 0.6, 0.4, 0.6, 0.8, 0.3, 0.4, 0.3, 0.3, 0.8, 0.8, 0.6, 0.8, 0.3, 0.6, 0.3, 0.8, 0.4, 0.4, 0.3, 0.8, 0.9, 0.5, 0.3, 0.5, 0.9, 0.3, 0.7, 0.7, 0.6, 0.5, 0.4, 0.4, 0.4, 0.6, 0.6, 0.9, 0.4, 0.4, 0.5, 0.5, 0.6, 0.7, 0.5, 0.7, 0.4, 0.8, 0.9, 0.9, 0.5, 0.8, 0.4, 0.9, 0.7, 0.3, 0.3, 0.4, 0.7, 0.7, 0.3, 0.8, 0.5, 0.5, 0.9, 0.9, 0.4, 0.9, 0.3, 0.8, 0.7, 0.7, 0.6, 0.4, 0.7, 0.4, 0.9, 0.8, 0.6, 0.5, 0.6, 0.9, 0.4, 0.9, 0.8, 0.5, 0.8, 0.6, 0.3, 0.3, 0.7, 0.3, 0.6, 0.6, 0.5, 0.8, 0.8, 0.6, 0.5, 0.4, 0.4, 0.8, 0.6, 0.8, 0.5, 0.8, 0.3, 0.6, 0.4, 0.5, 0.3]
    else:
        k = [k_param for _ in dag.nodes]
    dag.set_k(k)

    dag.rta_fcp(65536)

    if method == 'Wait-sufficient':
        WaitSufficient.allocate_ccs(dag.nodes)
    elif method == 'Decision-method':
        DecisionMethod.allocate_ccs(dag.nodes)
    elif method == 'Work-load':
        work_load(dag.nodes)
    elif method == 'Basic':
        Basic.allocate_ccs(dag.nodes)
    elif method == 'Allocate-available' or method == 'rta-cpf-eo':
        AllocateAvailable.allocate_ccs(dag.nodes)
    else:
        print('invalid-method')
        sys.exit()

    # print(time.perf_counter() - start)

    # JSONexport(dag)

    # p=[]
    #for node in dag.nodes:
    #    print('idx: '+str(node.idx).ljust(2)+', CC: '+str(node.cc_idx)+', time: '+str(node.time+node.sc()).ljust(3)+', exec_time: '+str(node.sc()).ljust(3))
        #if node.p in p:
        #    print('idx: '+str(node.idx).ljust(2)+', priority: '+str(node.p))
        #else:
        #    p.append(node.p)
    # ', n: '+str(node.core_idx)+
    makespan = 0
    for node in dag.nodes:
        if node.snk is True:
            makespan = node.start_time+node.amdahl_exec_time()

    return makespan
