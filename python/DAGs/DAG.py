from DAGs.DAG_Constructer import DAG_Constructer
from DAGs.DAG_base import Node, DAG_base

class DAG(DAG_base):
    # ＜コンストラクタ＞

    def __init__(self, nodes: list[Node]):
        """
        nodes: ノード
        """

        self.nodes: list[Node] = nodes
        self.set_critical_path()

    def rta_fcp(self, p):
        """
        拡張元手法の優先度決定手法
        """
        priority = p
        # クリティカルパスに高い優先度を割り当て
        for cp in self.critical_path:
            self.nodes[cp].p=priority
            priority-=1
        for cp in self.critical_path:
            # クリティカルパスを阻害する要素を前、終了が遅いから高い優先度を割り当てていく
            for p in sorted(self.nodes[cp].pre, key=lambda u: self.nodes[u].wcft, reverse=True):
                # クリティカルノードをsub_dag_nodesとして列挙
                sub_dag_nodes: list[int] = [a for a in self.search_ans(p) if a not in self.critical_path]
                sub_dag_nodes.append(p)

                nodes: list[Node] = []
                # sub_dag_nodesをDAGと見なし再帰的に優先度決定
                for i in sub_dag_nodes:
                    node = self.nodes[i]
                    tmp = Node()
                    tmp.set(node.idx, node.c, node.n, node.k)
                    # sub_dag_nodesに含まれnodeの前任であるものについて、sub_dag_nodes上での配列番目を取得する
                    # sub_dagではsub_dag_nodesの順にnodeの配列ができるので、これによってsub_dag上での前任が取得できる
                    tmp.pre = [sub_dag_nodes.index(p) for p in node.pre if p in sub_dag_nodes]
                    tmp.suc = [sub_dag_nodes.index(s) for s in node.suc if s in sub_dag_nodes]
                    nodes.append(tmp)
                sub_dag = DAG_Constructer.create_dag_node_from_nodes(nodes)

                # sub_dagの優先度決定
                priority = sub_dag.rta_fcp(priority)
                # sub_dagと元DAGのidxが同じものは優先度を同期（ただし優先度が高い方優先）
                for node in self.nodes:
                    for node2 in sub_dag.nodes:
                        if node.idx == node2.idx and node.p < node2.p:
                            node.p = node2.p
        return priority
    
    def checksum(self):
        checklist = {}
        for n in self.nodes:
            if str(n.p) in checklist:
                checklist[str(n.p)].append(n.idx)
            else:
                checklist[str(n.p)] = [n.idx]
        print(checklist)
