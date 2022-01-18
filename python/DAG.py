from DAGs.DAG_TGFF_load import DAG_TGFF
from DAGs.DAG_CPC import DAG_CPC
from DAGs.DAG_base import Node

class DAG(DAG_TGFF, DAG_CPC):
    # ＜コンストラクタ＞
    def __init__(self):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''

        super(DAG, self).__init__()

    def rta_fcp(self, p):
        priority = p
        for cp in self.critical_path:
            self.nodes[cp].p=priority
            priority-=1
        for cp in self.critical_path:
            for p in sorted(self.nodes[cp].pre, key=lambda u: self.nodes[u].wcft, reverse=True):
                branch = [ a for a in self.search_ans(p) if a not in self.critical_path ]
                branch.append(p)

                dag  = DAG()
                for n in self.nodes:
                    if n is not None and n.idx in branch:
                        tmp = Node()
                        tmp.set(n.idx, n.c, n.n, n.k)
                        tmp.pre = [p for p in n.pre if p in branch]
                        tmp.suc = [s for s in n.suc if s in branch]
                        dag.nodes.append(tmp)
                    else:
                        dag.nodes.append(None)

                dag.record_src_snk()
                dag.find_critical_path()
                priority = dag.rta_fcp(priority)
                for i in dag.nodes:
                    if i is not None and self.nodes[i.idx].p < i.p:
                        self.nodes[i.idx].p = i.p
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
