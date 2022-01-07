from DAG import DAG

test_dag = DAG()
test_dag.read_file_tgff("original_20_6")
test_dag.record_pre_suc()
test_dag.record_src_snk()
#test_dag.check()
test_dag.find_critical_path()
test_dag.print_critical_path()


#print("==========")
#print([t for t in test if t not in test_dag.nodes])
test_dag.rta_fcp()
for node in test_dag.nodes:
    print(str(node.idx).ljust(2)+" : "+str(node.p))