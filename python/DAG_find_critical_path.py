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


    def find_critical_path(self):
        for node in self.nodes:
            if node.src == 1:
                src = node
            if node.snk == 1:
                snk = node

        self.culc_wcst(src, 0)

        for i,node in enumerate(self.nodes):
            print(i,":",node.c)

        node = snk
        while(node.src == 0):
            self.critical_path.append(node.idx)
            tmp = src
            for p in node.pre:
                if tmp.wcst <= self.nodes[p].wcst:
                    tmp = self.nodes[p]
            node = tmp
        
    def culc_wcst(self, node, start_time):
        if node.wcst <= start_time:
            node.wcst = start_time
            for s in node.suc:
                self.culc_wcst(self.nodes[s], start_time + node.c)


    def print_critical_path(self):
        print(self.critical_path)