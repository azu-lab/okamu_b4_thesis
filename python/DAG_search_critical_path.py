from DAG_base import DAG_base

class DAG_SCP(DAG_base):
    # ＜コンストラクタ＞
    def __init__(self, file_tgff):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''
        critical_path=[]
        super(DAG_SCP, self).__init__(file_tgff)


    def search_critical_path(self):
        a=0

    def print_critical_path(self):
        print(critical_path)