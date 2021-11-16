from .DAG_find_critical_path import DAG_FCP, Node
from .DAG_base import idx_list

class DAG_CPC(DAG_FCP):
    # ＜コンストラクタ＞
    def __init__(self, file_tgff):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''
        self.provider=[]
        self.consumer_f=[]
        self.consumer_g=[]
        super(DAG_CPC, self).__init__(file_tgff)

    def construct_provider(self):
        idx = 0
        cp = self.critical_path[idx]
        while(1):
            tmp = [cp]
            idx += 1
            if idx < len(self.critical_path):
                cp = self.critical_path[idx]
            else:
                self.provider.append(tmp)
                break
            while(len(cp.pre) == 1):
                tmp.append(cp)
                idx += 1
                if idx < len(self.critical_path):
                    cp = self.critical_path[idx]
                else:
                    break
            self.provider.append(tmp)

    def construct_consumer(self):
        n_cp = self.critical_path
        for theta in self.provider:
            # ancesstorを取得
            f_theta = self.search_ans(theta[0].pre)
            # クリティカルパスと既にカウントしたものは除外
            f_theta = [f_t for f_t in f_theta if f_t.idx not in idx_list(n_cp)]
            n_cp.extend(f_theta)
            self.consumer_f.append(f_theta)

    def print_provider(self):
        for theta in self.provider:
            print(idx_list(theta))

    def print_consumer(self):
        for f_theta in self.consumer_f:
            print(idx_list(f_theta))