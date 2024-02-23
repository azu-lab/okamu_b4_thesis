from numpy import argmax
from numpy import argmin
from math import ceil
from .DAGs.DAG_base import Node
from enum import Enum

class Method(Enum):
    Wait_suff = 0
    Al_avail = 1
    Dec_method = 2
    Basic = 3

def Al_CCs(dags: list[Node], method=Method.Wait_suff):
    # initialize
    wait_queue: list[Node] = []
    executing_nodes: list[Node] = []
    vacant_core: list[int] = [ 16 for i in range(5) ]
    cores: list[list[int]] = [ [ i for i in range(16) ] for i in range(5) ]

    time: int = 0

    dags[0].start_time = 0
    dags[0].st_flag = True
    wait_queue.append(dags[0])

    while True:
        
        # allocation
        while len(wait_queue) > 0:
            v_h = wait_queue.pop(0)
            #print([99 if i < v_h.n else i for i in vacant_core])
            if method is not Method.Basic:
                cc_idx = argmin([99 if core_num < v_h.n else core_num for core_num in vacant_core])
            else:
                cc_idx = argmin([99 if core_num != 16 else core_num for core_num in vacant_core])
            if vacant_core[cc_idx] >= v_h.n:
                v_h.cc_idx = cc_idx
                v_h.start_time = time
                vacant_core[cc_idx] -= v_h.n
                for i in range(v_h.n):
                    v_h.core_idx.append(cores[cc_idx].pop(0))
                executing_nodes.append(v_h)
            else:
                if method is Method.Wait_suff or method is Method.Basic:
                    wait_queue.insert(0, v_h)
                    break
                elif method is Method.Al_avail:
                    cc_idx = argmax(vacant_core)
                    if vacant_core[cc_idx] != 0:
                        v_h.n = vacant_core[cc_idx]
                        v_h.cc_idx = cc_idx
                        v_h.start_time = time
                        vacant_core[cc_idx] -= v_h.n
                        for i in range(v_h.n):
                            v_h.core_idx.append(cores[cc_idx].pop(0))
                        executing_nodes.append(v_h)
                    else:
                        wait_queue.insert(0, v_h)
                        break
                elif method is Method.Dec_method:
                    cc_idx = argmax(vacant_core)
                    al_avail_flag = True
                    if vacant_core[cc_idx] != 0:
                        core_num = vacant_core[cc_idx]
                        tmp_time = time + v_h.amdahl_exe_time_with_n_core(core_num)

                        for node in sorted([node for node in executing_nodes if node.cc_idx == cc_idx], key=lambda u: u.start_time+u.amdahl_exec_time()):
                            core_num += node.n
                            if tmp_time > node.start_time+node.amdahl_exec_time()+v_h.amdahl_exe_time_with_n_core(core_num):
                                al_avail_flag = False
                    else:
                        al_avail_flag = False

                    if al_avail_flag is True:
                        v_h.n = vacant_core[cc_idx]
                        v_h.cc_idx = cc_idx
                        v_h.start_time = time
                        vacant_core[cc_idx] -= v_h.n
                        for i in range(v_h.n):
                            v_h.core_idx.append(cores[cc_idx].pop(0))
                        executing_nodes.append(v_h)
                    else:
                        wait_queue.insert(0, v_h)
                        break

                else:
                    print('invalid-method')
                    exit()
                

        # simulation
        # 早く終わる順に並び変え
        executing_nodes = sorted(executing_nodes, key=lambda node: node.start_time+node.amdahl_exec_time())
        while True:
            # 最も早く終わるものを取得し、終了をフラグ
            earliest = executing_nodes.pop(0)
            earliest.fn_flag = True

            # コア状況を更新（終了した分を戻す）
            vacant_core[earliest.cc_idx] += earliest.n
            cores[earliest.cc_idx].extend(earliest.core_idx)

            # 時刻の更新
            time = earliest.start_time + earliest.amdahl_exec_time()

            # 同じ時刻に完了するノードがあったら続行
            if len(executing_nodes) == 0 or executing_nodes[0].start_time + executing_nodes[0].amdahl_exec_time() != time:
                break

        # 開始しておらず全ての前任が終わったノードを検出
        new_entry: list[Node] = []
        for node in dags:
            # 開始しておらず
            if node.st_flag is True:
                continue

            # 前任
            pre_nodes = [dags[p] for p in node.pre]
            # 全ての前任が終わっていたら
            if all([n.fn_flag for n in pre_nodes]):
                node.st_flag = True
                new_entry.append(node)

        # 待機キューに追加
        wait_queue.extend(sorted(new_entry, key=lambda u: u.p, reverse=True))

        # 末尾ノードが実行完了したらループ終了
        if earliest.snk is True:
            break
