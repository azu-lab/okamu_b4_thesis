from DAG import DAG

test_dag = DAG("original_20_0")
test_dag.find_critical_path()
test_dag.print_critical_path()