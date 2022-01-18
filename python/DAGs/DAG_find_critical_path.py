from .DAG_base import DAG_base, Node
from .DAG_base import idx_list

class DAG_FCP(DAG_base):
    # ＜コンストラクタ＞
    def __init__(self):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''
        self.critical_path=[]
        super(DAG_FCP, self).__init__()

    # クリティカルパスの特定
    def find_critical_path(self):
        # ソースとシンクの特定（DAGなら戦闘と末尾でも可）
        for n in self.nodes:
            if n is not None:
                if n.src == 1:
                    src = n.idx
                if n.snk == 1:
                    snk = n.idx

        # 最悪ケースの開始時間の設定
        self.culc_wcft(src, 0)

        # 動作テスト
        #for i,node in enumerate(self.nodes):
        #    print(i,":",node.c)

        # 末尾から、snkに最悪ケースの開始時間を与えるノードを特定
        i = snk
        while(self.nodes[i].src == 0):
            self.critical_path.append(i)
            tmp = src
            for p in self.nodes[i].pre:
                if self.nodes[tmp].wcft <= self.nodes[p].wcft:
                    tmp = p
            i = tmp
        self.critical_path.append(src)

        self.critical_path.reverse()
        
    # 最悪ケースの開始時間の設定
    def culc_wcft(self, i, start_time):
        # 最悪ケースの開始時間が更新されたら
        if self.nodes[i].wcft <= start_time + self.nodes[i].sc():
            self.nodes[i].wcft = start_time + self.nodes[i].sc()
            # 自分の後ろも更新する
            for s in self.nodes[i].suc:
                if s is not None:
                    self.culc_wcft(s, start_time + self.nodes[s].sc())


    def print_critical_path(self):
        print(self.critical_path)