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

        self.idx: int = 0
        self.c: int = 0
        self.n: int = 1
        self.p: int = 0
        self.k: float = 1.0

        self.comm: list[int] = []
        self.pre: list[int] = []
        self.suc: list[int] = []
        self.src: bool = False
        self.snk: bool = False

        self.cc_idx: int = -1
        self.core_idx: list[int] = []
        self.time: int = -1
        self.fn_flag: bool = False
        self.st_flag: bool = False

        # クリティカルパス探索で使用
        self.wcft: int = 0

    def sc(self) -> int:
        return ceil(((1-self.k)+self.k/self.n)*self.c)

    def sc_n(self, n: int) -> int:
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
        self.nodes: list[Node] = []
        self.critical_path: list[int] = []

    def record_src_snk(self):
        snk: list[Node] = []
        for node in self.nodes:
            # srcノードを求める
            if(len(node.pre) == 0):
                node.src = True
            # snkノードを求める
            if(len(node.suc) == 0):
                node.snk = True
                snk.append(node)

        snksnk = snk.pop(-1)
        for s in snk:
            s.suc.append(self.nodes.index(snksnk))
            snksnk.pre.append(self.nodes.index(s))
            s.snk=False

    def search_ans(self, idx: int) -> list[int]:
        ans: list[int] = []
        for p in self.nodes[idx].pre:
            ans.append(p)
            ans.extend(self.search_ans(p))

        return ans

    def search_des(self, idx: int) -> list[int]:
        des: list[int] = []
        for s in self.nodes[idx].suc:
            des.append(s)
            des.extend(self.search_des(s))

        return des

    def set_n(self, n: list[int]):
        for i in range(len(self.nodes)):
            self.nodes[i].n = n[i]

    def set_k(self, k: list[int]):
        for i in range(len(self.nodes)):
            self.nodes[i].k = k[i]

    def check(self):
        print(idx_list(self.nodes[2].pre))

def idx_list(nodes):
    return [node.idx for node in nodes]