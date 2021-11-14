from DAG_TGFF_load import DAG_TGFF

test_dag = DAG_TGFF("original_10_0")
test_dag.read_file_tgff()
test_dag.check()