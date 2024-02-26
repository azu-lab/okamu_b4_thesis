from math import ceil

class Node:
    def __init__(self):
        """
        p:   優先度
        pre: 前任タスクの配列番目
        suc: 後任タスクの配列番目

        cc_idx:     割り当てクラスタ番目
        core_idx:   割り当てコア番目（クラスタ内）
        start_time: 開始時刻
        """

        self.idx: int = 0
        self.c: int = 0
        self.n: int = 1
        self.p: int = 0
        self.k: float = 1.0

        self.pre: list[int] = []
        self.suc: list[int] = []
        self.src: bool = False
        self.snk: bool = False

        self.cc_idx: int = -1
        self.core_idx: list[int] = []
        self.start_time: int = -1
        self.fn_flag: bool = False
        self.st_flag: bool = False

        self.wcft: int = 0 # クリティカルパス探索・優先度決定で使用

    def amdahl_exec_time(self) -> int:
        """
        アムダールの法則による実行時間
        現在割り当てられたコア数・並列度に基づく
        """
        return ceil(((1-self.k)+self.k/self.n)*self.c)

    def amdahl_exe_time_with_n_core(self, n: int) -> int:
        """
        アムダールの法則による実行時間
        引数のコア数・並列度に基づく
        """
        return ceil(((1-self.k)+self.k/n)*self.c)

    def set(self, idx: int, c: int, n: int, k: float):
        """
        idx: ノード識別子（配列の番号とは別の一意の値）
        c:   1コアでの実行時間
        n:   コア割り当て数
        k:   並列割合（アムダールの法則）
        """
        self.idx = idx
        self.c = c
        self.n = n
        self.k = k


# DAG
class DAG_base:
    # ＜コンストラクタ＞
    def __init__(self):
        self.nodes: list[Node] = []

    def search_ans(self, idx: int) -> list[int]:
        """
        祖先を検索
        """
        ans: list[int] = []
        for p in self.nodes[idx].pre:
            ans.append(p)
            ans.extend(self.search_ans(p))

        return ans

    def search_des(self, idx: int) -> list[int]:
        """
        子孫を検索
        """
        des: list[int] = []
        for s in self.nodes[idx].suc:
            des.append(s)
            des.extend(self.search_des(s))

        return des

    def set_n(self, n: list[int]):
        """
        n:   コア割り当て数
        """
        for i in range(len(self.nodes)):
            self.nodes[i].n = n[i]
        self.set_critical_path()

    def set_k(self, k: list[int]):
        """
        k:   並列割合（アムダールの法則）
        """
        for i in range(len(self.nodes)):
            self.nodes[i].k = k[i]
        self.set_critical_path()

    # 最悪ケースの開始時間の設定
    def _culc_wcft(self, i: int, start_time: int):
        # 最悪ケースの開始時間が更新されたら
        if self.nodes[i].wcft <= start_time + self.nodes[i].amdahl_exec_time():
            self.nodes[i].wcft = start_time + self.nodes[i].amdahl_exec_time()
            # 自分の後ろも更新する
            for s in self.nodes[i].suc:
                if s is not None:
                    self._culc_wcft(s, start_time + self.nodes[s].amdahl_exec_time())

    
    def set_critical_path(self):
        """
        クリティカルパスの特定
        """
        self.critical_path: list[int] = []
        # ソースとシンクの特定（DAGなら戦闘と末尾でも可）
        for i, node in enumerate(self.nodes):
            if node.src == True:
                src = i
            if node.snk == True:
                snk = i

        # 最悪ケースの開始時間の設定
        self._culc_wcft(src, 0)

        # 末尾から、snkに最悪ケースの開始時間を与えるノードを特定
        i: int = snk
        while(self.nodes[i].src == False):
            self.critical_path.append(i)
            tmp = src
            for p in self.nodes[i].pre:
                if self.nodes[tmp].wcft <= self.nodes[p].wcft:
                    tmp = p
            i = tmp
        self.critical_path.append(src)

        self.critical_path.reverse()

    def print_critical_path(self):
        print(self.critical_path)

    def check(self):
        print(idx_list(self.nodes[2].pre))

def idx_list(nodes):
    return [node.idx for node in nodes]