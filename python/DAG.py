from DAGs.DAG_Constructer import DAG_Constructer
from DAGs.DAG_CPC import DAG_CPC, DAG_FCP
from DAGs.DAG_base import Node

class DAG(DAG_FCP):
    # ＜コンストラクタ＞

    def __init__(self, file_name: str | None = None):
        '''
        file_name : .tgffファイルの名前
        nodes[]: ノードの集合
        '''
        if file_name:
            self.nodes: list[Node] = DAG_Constructer.create_dag_from_tgff_file(file_name)
        else:
            self.nodes: list[Node] = []
        self.critical_path: list[int] = []

    def rta_fcp(self, p):
        priority = p
        for cp in self.critical_path:
            self.nodes[cp].p=priority
            priority-=1
        for cp in self.critical_path:
            for p in sorted(self.nodes[cp].pre, key=lambda u: self.nodes[u].wcft, reverse=True):
                branch: list[Node] = [self.nodes[a] for a in self.search_ans(p) if a not in self.critical_path]
                branch.append(self.nodes[p])
                branch_idx = [self.nodes.index(b) for b in branch]

                nodes: list[Node] = []
                for node in branch:
                    tmp = Node()
                    tmp.set(node.idx, node.c, node.n, node.k)
                    tmp.pre = [branch_idx.index(p) for p in node.pre if p in branch_idx]
                    tmp.suc = [branch_idx.index(s) for s in node.suc if s in branch_idx]
                    nodes.append(tmp)
                dag = DAG()
                dag.nodes = DAG_Constructer.create_dag_from_nodes(nodes)

                dag.find_critical_path()
                priority = dag.rta_fcp(priority)
                for node in self.nodes:
                    for node2 in dag.nodes:
                        if node.idx == node2.idx and node.p < node2.p:
                            node.p = node2.p
                """self.nodes[p].p=priority
                for ans in self.search_ans(p):
                    if self.nodes[ans].p < priority:
                        self.nodes[ans].p=priority"""
                priority-=1
        return priority
    
    def checksum(self):
        checklist = {}
        for n in self.nodes:
            if str(n.p) in checklist:
                checklist[str(n.p)].append(n.idx)
            else:
                checklist[str(n.p)] = [n.idx]
        print(checklist)
