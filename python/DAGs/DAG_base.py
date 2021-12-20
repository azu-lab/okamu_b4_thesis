# -*- coding: utf-8 -*-


import pprint

class Node:
    def __init__(self):
        """
        c : niの実行時間
        comm[j] : ni~nj間の通信時間
        pre[i] : niの前任ノードのリスト
        suc[i] : niの後続ノードのリスト
        src[i]=1 : niはsrcノード. src[i]=0 : niはsrcノードではない
        snk[i]=1 : niはsnkノード. snk[i]=0 : niはsnkノードではない
        """

        self.idx=0
        self.c=0
        self.comm=[]
        self.pre=[]
        self.suc=[]
        self.src=0
        self.snk=0

        # クリティカルパス探索で使用
        self.wcst=0


# DAG
class DAG_base:
    # ＜コンストラクタ＞
    def __init__(self, file_tgff):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''
        self.nodes = []
        self.file_name = file_tgff
        

    # ＜メソッド＞
    # .tgffファイルの読み込み
    # def read_file_tgff(self): DAG_TGFF_load.

    def record_pre_suc(self):
        for begin, node in enumerate(self.nodes):
            # エッジを検出し, preとsucを記録
            for end, comm in enumerate(node.comm):
                if comm != 0:
                    node.suc.append(self.nodes[end])
                    self.nodes[end].pre.append(node)

    def search_src_snk(self):
        for node in self.nodes:
            # srcノードを求める
            if(len(node.pre) == 0):
                    node.src = 1
            # snkノードを求める
            if(len(node.suc) == 0):
                    node.snk = 1

    def search_ans(self, nodes):
        ans = []
        for node in nodes:
            ans.append(node)
            ans.extend(self.search_ans(node.pre))

        return ans

    def search_des(self, nodes):
        des = []
        for node in nodes:
            des.append(node)
            des.extend(self.search_des(node.suc))

        return des

    def check(self):
        print(idx_list(self.nodes[2].pre))

def idx_list(nodes):
    return [node.idx for node in nodes]