from DAG_TGFF_load import DAG_TGFF
from DAG_search_critical_path import DAG_SCP

class DAG(DAG_TGFF, DAG_SCP):
    # ＜コンストラクタ＞
    def __init__(self, file_tgff):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        nodes[]: ノードの集合
        '''

        super(DAG, self).__init__(file_tgff)