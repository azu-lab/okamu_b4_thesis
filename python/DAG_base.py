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
    # def read_file_tgff(self): DAG_TGFF_load.pyにて

    def check(self):
        print(self.nodes[2].pre)