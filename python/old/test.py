from DAGs.DAG_Constructer import DAG_Constructer

test_dag = DAG_Constructer.create_dag_from_tgff_file("./DAG/original_20_6.tgff")
#test_dag.check()
test_dag.set_critical_path()
test_dag.print_critical_path()


#print("==========")
#print([t for t in test if t not in test_dag.nodes])
test_dag.rta_fcp(65536)
test_dag.nodes.sort(key=lambda x: x.p)
for i, n in enumerate(test_dag.nodes):
    n.p = i
test_dag.nodes.sort(key=lambda x: x.idx)

for node in test_dag.nodes:
    print(str(node.idx).ljust(2)+" : "+str(node.p))