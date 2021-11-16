from DAG import DAG

test_dag = DAG("original_20_6")
test_dag.read_file_tgff()
test_dag.record_pre_suc()
test_dag.search_src_snk()
#test_dag.check()
test_dag.find_critical_path()
#test_dag.print_critical_path()
test_dag.construct_provider()
test_dag.print_provider()
print("========")
test_dag.construct_consumer()
test_dag.print_consumer()

test = []
for p in test_dag.provider:
    test.extend(p)
for c in test_dag.consumer_f:
    test.extend(c)

print("==========")
print([t for t in test if t not in test_dag.nodes])