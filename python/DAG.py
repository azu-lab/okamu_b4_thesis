from DAGs.DAG_TGFF_load import DAG_TGFF
from DAGs.DAG_CPC import DAG_CPC

class DAG(DAG_TGFF, DAG_CPC):
    # ＜コンストラクタ＞
    def __init__(self):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''

        super(DAG, self).__init__()

    def rta_fcp(self):
        priority = 65536
        for cp in self.critical_path:
            self.nodes[cp].p=priority
            priority-=1
        for cp in self.critical_path:
            for p in sorted(self.nodes[cp].pre, key=lambda u: self.nodes[u].wcft, reverse=True):
                self.nodes[p].p=priority
                priority-=1
                for ans in self.search_ans(p):
                    if self.nodes[ans].p < priority:
                        self.nodes[ans].p=priority
                        priority-=1