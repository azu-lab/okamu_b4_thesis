from DAG import DAG

test_dag = DAG("original_20_6")
test_dag.read_file_tgff()
#test_dag.check()
test_dag.find_critical_path()
test_dag.construct_provider()
test_dag.print_provider()
test_dag.construct_consumer()
test_dag.print_consumer()