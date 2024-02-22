from .DAG_base import DAG_base, Node
from .DAG_base import idx_list

class DAG_CPC(DAG_base):
    """
    論文では使っていないのでリファクタリングしていない。
    参考資料&実験用
    """
    # ＜コンストラクタ＞
    def __init__(self):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''
        self.provider=[]
        self.consumer_f=[]
        self.consumer_g=[]

    def construct_provider(self):
        idx = 0
        while(1):
            tmp = [self.critical_path[idx]]
            idx += 1
            if idx >= len(self.critical_path):
                self.provider.append(tmp)
                break
            while(len(self.nodes[self.critical_path[idx]].pre) == 1):
                tmp.append(self.critical_path[idx])
                idx += 1
                if idx >= len(self.critical_path):
                    break
            self.provider.append(tmp)

    def construct_consumer(self):
        n_cp = self.critical_path
        for theta in self.provider:
            # consumer_f
            # ancesstorを取得
            f_theta = self.search_ans(theta[0].pre)
            # クリティカルパスと既にカウントしたものは除外
            f_theta = [f_t for f_t in f_theta if f_t.idx not in idx_list(n_cp)]
            n_cp.extend(f_theta)
            self.consumer_f.append(f_theta)

            # consumer_g
            g_theta = [n for n in self.nodes if n.idx not in idx_list(n_cp)]
            self.consumer_g.append(g_theta)
            for f_t in f_theta:
                g_theta = [g for g in g_theta if g.idx not in idx_list(self.search_ans(f_t.pre))]
                g_theta = [g for g in g_theta if g.idx not in idx_list(self.search_des(f_t.suc))]

    def print_provider(self):
        for theta in self.provider:
            print(theta)

    def print_consumer_f(self):
        for f_theta in self.consumer_f:
            print(f_theta)

    def print_consumer_g(self):
        for g_theta in self.consumer_g:
            print(g_theta)