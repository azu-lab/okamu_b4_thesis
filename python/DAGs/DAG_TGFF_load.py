from .DAG_base import Node


# DAG
class DAG_Constructer:
    # ＜コンストラクタ＞
    def __init__(self):
        pass

    # ＜メソッド＞
    @staticmethod
    def create_dag_from_tgff_file(file_path) -> list[Node]:
        """
        .tgffファイルの読み込み
        返り値はNode配列なので注意
        先輩から引き継いだもののためリファクタリングはしていない、新しく研究を行う場合、RD-Genを使うこと推奨
        """
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

        nodes: list[Node] = []

        # 実行時間を取得
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ

            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            if(line_list[0] == 'TASK'):
                node = Node()
                node.c = type_cost[int(line_list[3])] #line_list[3]がTYPEなので、それに対応する実行時間を格納
                node.idx = len(nodes)
                nodes.append(node)

        # num_of_node = len(nodes)  # タスク数を取得

        file_tgff.close()
        file_tgff = open(file_path, "r")

        comms: list[list[int]] = []
        # エッジの通信時間を取得
        # for node in nodes:
        #     node.comm = [0] * num_of_node

        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ

            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            if(line_list[0] == 'ARC'):
                from_t = int(line_list[3][3:])  # エッジを出すタスク
                to_t = int(line_list[5][3:])  # エッジの先のタスク
                # comm_cost = int(type_cost[int(line_list[7])])  # TYPEに書かれている時間を通信時間とする
                # nodes[from_t].comm[to_t] = comm_cost
                comms.append([from_t, to_t])

        file_tgff.close()

        nodes = DAG_Constructer._pre_suc_setted_nodes(nodes, comms)

        return nodes

    @staticmethod
    def _pre_suc_setted_nodes(nodes: list[Node], comms: list[list[int]]) -> list[Node]:
        for comm in comms:
            src = comm[0]
            dst = comm[1]
            for i, node in enumerate(nodes):
                if i == src:
                    node.suc.append(dst)
                if i == dst:
                    node.pre.append(src)
        return nodes