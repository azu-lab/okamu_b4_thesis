from DAG_base import DAG_base, Node

class DAG_FCP(DAG_base):
    # ＜コンストラクタ＞
    def __init__(self, file_tgff):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''
        self.critical_path=[]
        super(DAG_FCP, self).__init__(file_tgff)

    # クリティカルパスの特定
    def find_critical_path(self):
        # ソースとシンクの特定（DAGなら戦闘と末尾でも可）
        for node in self.nodes:
            if node.src == 1:
                src = node
            if node.snk == 1:
                snk = node

        # 最悪ケースの開始時間の設定
        self.culc_wcst(src, 0)

        # 動作テスト
        #for i,node in enumerate(self.nodes):
        #    print(i,":",node.c)

        # 末尾から、snkに最悪ケースの開始時間を与えるノードを特定
        node = snk
        while(node.src == 0):
            self.critical_path.append(node)
            tmp = src
            for p in node.pre:
                if tmp.wcst <= p.wcst:
                    tmp = p
            node = tmp
        self.critical_path.append(src)

        self.critical_path.reverse()
        
    # 最悪ケースの開始時間の設定
    def culc_wcst(self, node, start_time):
        # 最悪ケースの開始時間が更新されたら
        if node.wcst <= start_time:
            node.wcst = start_time
            # 自分の後ろも更新する
            for s in node.suc:
                self.culc_wcst(s, start_time + node.c)


    def print_critical_path(self):
        print([cp.idx for cp in self.critical_path])