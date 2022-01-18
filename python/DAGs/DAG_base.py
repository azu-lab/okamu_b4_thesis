# -*- coding: utf-8 -*-


import pprint
from math import ceil

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
        self.n=1
        self.p=0
        self.k=1.0

        self.comm=[]
        self.pre=[]
        self.suc=[]
        self.src=False
        self.snk=False

        self.cc_idx=-1
        self.core_idx=[]
        self.time=-1
        self.fn_flag=False
        self.st_flag=False

        # クリティカルパス探索で使用
        self.wcft=0

    def sc(self):
        return ceil(((1-self.k)+self.k/self.n)*self.c)

    def sc_n(self, n: int):
        return ceil(((1-self.k)+self.k/n)*self.c)

    def set(self, idx: int, c: int, n: int, k: float):
        self.idx = idx
        self.c = c
        self.n = n
        self.k = k


# DAG
class DAG_base:
    # ＜コンストラクタ＞
    def __init__(self):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''
        self.nodes = []
        

    # ＜メソッド＞
    # .tgffファイルの読み込み
    # def read_file_tgff(self): DAG_TGFF_load.

    def record_pre_suc(self):
        for begin, node in enumerate(self.nodes):
            # エッジを検出し, preとsucを記録
            for end, comm in enumerate(node.comm):
                if comm != 0:
                    node.suc.append(end)
                    self.nodes[end].pre.append(begin)

    def record_src_snk(self):
        snk = []
        for node in self.nodes:
            if node is not None:
                # srcノードを求める
                if(len(node.pre) == 0):
                        node.src = True
                # snkノードを求める
                if(len(node.suc) == 0):
                        node.snk = True
                        snk.append(node)

        snksnk = snk.pop(-1)
        for s in snk:
            s.suc.append(snksnk.idx)
            snksnk.pre.append(s.idx)
            s.snk=False

    def search_ans(self, idx):
        ans = []
        for p in self.nodes[idx].pre:
            ans.append(p)
            ans.extend(self.search_ans(p))

        return ans

    def search_des(self, nodes):
        des = []
        for node in nodes:
            des.append(node)
            des.extend(self.search_des(node.suc))

        return des

    def set_n(self, n):
        for i in range(len(self.nodes)):
            self.nodes[i].n = n[i]

    def set_k(self, k):
        for i in range(len(self.nodes)):
            self.nodes[i].k = k[i]

    def check(self):
        print(idx_list(self.nodes[2].pre))

def idx_list(nodes):
    return [node.idx for node in nodes]