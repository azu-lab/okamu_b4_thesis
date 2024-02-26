from numpy import argmax, argmin
from .DAGs.DAG_base import Node
from abc import abstractclassmethod

from sys import maxsize as MAXSIZE

class MethodBase:
    """
    共通の手法・スケジューリングなど
    """
    # 1クラスタに含まれるコア数
    CLUSTER_LEN: int = 16
    # プロセッサに含まれるクラスタ数
    CLUSTER_NUM: int = 5

    @classmethod
    def allocate_ccs(cls, dags: list[Node]):
        # 初期化
        # 待機キュー
        wait_queue: list[Node] = []
        # 実行中ノードリスト
        executing_nodes: list[Node] = []
        # 各クラスタに割り当てられているノード数
        core_map: list[list[int]] = [ [ i for i in range(MethodBase.CLUSTER_LEN) ] for i in range(MethodBase.CLUSTER_NUM) ]

        # 現在時刻
        time: int = 0

        # 入口ノードを実行開始
        dags[0].start_time = 0
        dags[0].st_flag = True
        wait_queue.append(dags[0])

        while True:
            # タスクをコア（クラスタ）に割り当て、或いは割り当てずにスルー
            # 具体的な処理は各手法ごとのクラスのallicate関数に記載
            wait_queue, core_map, executing_nodes, time = cls.allocate(wait_queue, core_map, executing_nodes, time)

            # simulation
            # 早く終わる順に並び変え
            executing_nodes = sorted(executing_nodes, key=lambda node: node.start_time+node.amdahl_exec_time())
            while True:
                # 最も早く終わるものを取得し、終了をフラグ
                earliest = executing_nodes.pop(0)
                earliest.fn_flag = True

                # コア状況を更新（終了した分を戻す）
                core_map[earliest.cc_idx].extend(earliest.core_idx)

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

    @abstractclassmethod
    def allocate(cls, wait_queue: list[Node], core_map: list[list[int]], executing_nodes: list[Node], time: int) -> tuple[list[Node], list[list[int]], list[Node], int]:
        pass


class WaitSufficient(MethodBase):
    """
    十分なコアが空いているクラスタができるまで待つ
    """
    CLUSTER_LEN: int = 16
    CLUSTER_NUM: int = 5

    @classmethod
    def allocate(cls, wait_queue: list[Node], core_map: list[list[int]], executing_nodes: list[Node], time: int) -> tuple[list[Node], list[list[int]], list[Node], int]:
        while len(wait_queue) > 0:
            # 待ち行列から最優先を取得
            node_priory = wait_queue.pop(0)
            # 最優先の必要コアより多く空きがあるなかで最小のコアの番号を取得
            cc_idx = argmin([MAXSIZE if len(core_row) < node_priory.n else len(core_row) for core_row in core_map])

            # コアが足りる場合
            if len(core_map[cc_idx]) >= node_priory.n:
                # タスクに、クラスタ割り当て→コア割り当て→開始時間設定
                node_priory.cc_idx = cc_idx
                for _ in range(node_priory.n):
                    node_priory.core_idx.append(core_map[cc_idx].pop(0))
                node_priory.start_time = time
                # 実行中リストに追加
                executing_nodes.append(node_priory)

            # コアが足りない場合
            else:
                # 待機キューに戻す
                wait_queue.insert(0, node_priory)
                break

        return wait_queue, core_map, executing_nodes, time


class AllocateAvailable(MethodBase):
    """
    今最もコアが空いているクラスタに割り当てる（割り当て数を減らす）
    """
    CLUSTER_LEN: int = 16
    CLUSTER_NUM: int = 5

    @classmethod
    def allocate(cls, wait_queue: list[Node], core_map: list[list[int]], executing_nodes: list[Node], time: int) -> tuple[list[Node], list[list[int]], list[Node], int]:
        while len(wait_queue) > 0:
            # 待ち行列から最優先を取得
            node_priory = wait_queue.pop(0)
            # 最優先の必要コアより多く空きがあるなかで最小のコアの番号を取得
            cc_idx = argmin([MAXSIZE if len(core_row) < node_priory.n else len(core_row) for core_row in core_map])

            # コアが足りる場合
            if len(core_map[cc_idx]) >= node_priory.n:
                # タスクに、クラスタ割り当て→コア割り当て→開始時間設定
                node_priory.cc_idx = cc_idx
                for _ in range(node_priory.n):
                    node_priory.core_idx.append(core_map[cc_idx].pop(0))
                node_priory.start_time = time
                # 実行中リストに追加
                executing_nodes.append(node_priory)

            # コアが足りない場合
            else:
                # 最も空いているコアを取得
                cc_idx = argmax([len(core_row) for core_row in core_map])
                if len(core_map[cc_idx]) != 0:
                    # タスクに、クラスタ割り当て→割り当てコア数を変更→コア割り当て→開始時間設定
                    node_priory.cc_idx = cc_idx
                    node_priory.n = len(core_map[cc_idx])
                    for _ in range(node_priory.n):
                        node_priory.core_idx.append(core_map[cc_idx].pop(0))
                    node_priory.start_time = time
                    # 実行中リストに追加
                    executing_nodes.append(node_priory)
                else:
                    # 空き0コアだったら待機キューに戻す
                    wait_queue.insert(0, node_priory)
                    break

        return wait_queue, core_map, executing_nodes, time


class DecisionMethod(MethodBase):
    """
    今最も空いているクラスタに対し、割り当てられた各タスクが完了するまで待つのと
    今すぐ割り当てるのでどちらが早くタスクを完了するかを比較する
    """
    CLUSTER_LEN: int = 16
    CLUSTER_NUM: int = 5

    @classmethod
    def allocate(cls, wait_queue: list[Node], core_map: list[list[int]], executing_nodes: list[Node], time: int) -> tuple[list[Node], list[list[int]], list[Node], int]:
        while len(wait_queue) > 0:
            # 待ち行列から最優先を取得
            node_priory = wait_queue.pop(0)
            # 最優先の必要コアより多く空きがあるなかで最小のコアの番号を取得
            cc_idx = argmin([MAXSIZE if len(core_row) < node_priory.n else len(core_row) for core_row in core_map])

            if len(core_map[cc_idx]) >= node_priory.n:
                # タスクに、クラスタ割り当て→コア割り当て→開始時間設定
                node_priory.cc_idx = cc_idx
                for _ in range(node_priory.n):
                    node_priory.core_idx.append(core_map[cc_idx].pop(0))
                node_priory.start_time = time
                # 実行中リストに追加
                executing_nodes.append(node_priory)
            else:
                # 一番空いているコアを取得
                cc_idx = argmax([len(core_row) for core_row in core_map])

                al_avail_flag = True
                if len(core_map[cc_idx]) != 0:
                    core_num = len(core_map[cc_idx])
                    # 今空いているコアに割り当てた場合の時間
                    tmp_time = time + node_priory.amdahl_exe_time_with_n_core(core_num)

                    # cc_idxクラスタに割り当てられたノードnodeが完了した時刻に置いて
                    for node in sorted([node for node in executing_nodes if node.cc_idx == cc_idx], key=lambda u: u.start_time+u.amdahl_exec_time()):
                        # core_numコア（現在+nodeの利用分）空いている
                        core_num += node.n
                        # 今空いているコアに割り当てた場合の時間　と　nodeが完了してからcore_numコア（現在+nodeの利用分）で実行した場合の時間を比較
                        # nodeが完了してからの方が早い場合、今空いているコアフラグを折る
                        if tmp_time > node.start_time+node.amdahl_exec_time()+node_priory.amdahl_exe_time_with_n_core(core_num):
                            al_avail_flag = False
                else:
                    al_avail_flag = False

                # 今空いているコアに割り当てる
                if al_avail_flag is True:
                    # タスクに、クラスタ割り当て→割り当てコア数を変更→コア割り当て→開始時間設定
                    node_priory.cc_idx = cc_idx
                    node_priory.n = len(core_map[cc_idx])
                    for _ in range(node_priory.n):
                        node_priory.core_idx.append(core_map[cc_idx].pop(0))
                    node_priory.start_time = time
                    # 実行中リストに追加
                    executing_nodes.append(node_priory)
                else:
                    # 次を待つ
                    # 待機キューに戻す
                    wait_queue.insert(0, node_priory)
                    break

        return wait_queue, core_map, executing_nodes, time


class Basic(MethodBase):
    """
    クラスタが全部空いていれば割り当て、そうでなければ待つ（WaitSufficientの劣化）
    """
    CLUSTER_LEN: int = 16
    CLUSTER_NUM: int = 5

    @classmethod
    def allocate(cls, wait_queue: list[Node], core_map: list[list[int]], executing_nodes: list[Node], time: int) -> tuple[list[Node], list[list[int]], list[Node], int]:
        while len(wait_queue) > 0:
            # 待ち行列から最優先を取得
            node_priory = wait_queue.pop(0)
            # ノードが割り当てられていないクラスタを取得
            cc_idx = argmin([MAXSIZE if len(core_row) != MethodBase.CLUSTER_LEN else len(core_row) for core_row in core_map])

            # コアが足りる場合
            if len(core_map[cc_idx]) >= node_priory.n:
                # タスクに、クラスタ割り当て→コア割り当て→開始時間設定
                node_priory.cc_idx = cc_idx
                for _ in range(node_priory.n):
                    node_priory.core_idx.append(core_map[cc_idx].pop(0))
                node_priory.start_time = time
                # 実行中リストに追加
                executing_nodes.append(node_priory)

            # コアが足りない場合
            else:
                # 待機キューに戻す
                wait_queue.insert(0, node_priory)
                break

        return wait_queue, core_map, executing_nodes, time
