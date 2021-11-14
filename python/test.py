from DAG import DAG

test_dag = DAG("original_10_0")
test_dag.read_file_tgff()
test_dag.check()