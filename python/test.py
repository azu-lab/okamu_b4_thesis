from DAG_base import DAG_base

test_dag = DAG_base("original_10_0")
test_dag.read_file_tgff()
test_dag.check()