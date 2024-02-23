from ..DAGs.DAG_base import DAG_base
from ..DAGs.DAG_base import Node
import json
from math import ceil

def JSONexport(dag: DAG_base):
    # テスト用に作ったものなのでリファクタリングしてないです。悪しからず。
    json_data = {
        'coreNum': 80,
        'makespan':10000,
        'taskSet': []
    }

    for node in dag.nodes:
        for n in node.core_idx:
            json_element = {
                'coreID': int(node.cc_idx*16+n),
                'taskName': 'task_'+str(node.idx),
                'startTime': int(node.start_time),
                'executionTime': int(node.amdahl_exec_time())
            }
            json_data['taskSet'].append(json_element)

        if node.snk is True:
            json_data['makespan'] = int(node.start_time + ceil(node.c / node.n))

    json_file = open('output.json', 'w')
    json.dump(json_data, json_file)
    json_file.close()