# 卒業研究(okamu)

## ディレクトリ構成
- DAG.py
  - クラスDAG(実際に評価において使用したDAGモデル)を定義しています。
  - クラスDAGはDAG_TGFF及びDAG_SCPを継承しています。
- DAG_TGFF_load.py
  - クラスDAG_TGFF(.tgff読み込み対応DAGモデル)を定義しています。
  - load_DAG_from_TGFF関数により、各種メンバ変数の値を.tgffファイルからロードします。
  - クラスDAGはDAG_baseを継承しています。
- DAG_base.py
  - クラスDAG_base(全てのDAG_クラスの基底クラス)を定義しています。
- DAG_search_critical_path.py
  - DAG_SCP(クリティカルパス探索を行えるDAGモデル)を定義しています。
  - search_critical_path関数により、メンバ変数critical_pathにクリティカルパスを格納します。
