from .DAG_base import DAG_base, Node


# DAG
class DAG_TGFF(DAG_base):
    # ＜コンストラクタ＞
    def __init__(self):
        '''
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''

        super(DAG_TGFF, self).__init__()
        

    # ＜メソッド＞
    # .tgffファイルの読み込み
    def read_file_tgff(self, file_path):
        file_tgff = open(file_path, "r")
        
        type_cost = []  # TYPEと実行時間の対応関係の配列
        read_flag = 0  # PE5の情報だけを読み込むためのフラグ
        info_flag = 0   #余計な部分を読み込まないためのフラグ
        
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ
            
            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            # 読み込む範囲を限定
            if(len(line_list) >= 2):
                if(line_list[0] == '@PE' and line_list[1] == '5'):
                    read_flag = 1

                if(line_list[1] == 'type' and line_list[2] == 'exec_time'):
                    info_flag = 1
                    continue
                
                # TYPEの情報取得
                if(read_flag == 1 and info_flag == 1):
                    type_cost.append(int(float(line_list[1])))  #TYPEに対応する実行時間をint型で格納
                    
            elif(line_list[0] == '}'):
                read_flag = 0
                info_flag = 0
        
        file_tgff.close()
        
        # TASKの情報の取得
        file_tgff = open(file_path, "r")

        # 実行時間を取得
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ

            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            if(line_list[0] == 'TASK'):
                node = Node()
                node.c = type_cost[int(line_list[3])] #line_list[3]がTYPEなので、それに対応する実行時間を格納
                node.idx = len(self.nodes)
                self.nodes.append(node)

        self.num_of_node = len(self.nodes)  # タスク数を取得

        file_tgff.close()
        file_tgff = open(file_path, "r")

        # エッジの通信時間を取得
        for node in self.nodes:
            node.comm = [0] * self.num_of_node

        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ

            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            if(line_list[0] == 'ARC'):
                from_t = int(line_list[3][3:])  # エッジを出すタスク
                to_t = int(line_list[5][3:])  # エッジの先のタスク
                comm_cost = int(type_cost[int(line_list[7])])  # TYPEに書かれている時間を通信時間とする
                self.nodes[from_t].comm[to_t] = comm_cost

        file_tgff.close()
