# python
研究の評価に利用したプログラムです。

## ディレクトリ構成
- DAGs/
  - DAG_base: DAGの基本機能（ノードやクリティカルパス、祖先・子孫）を実装しています
  - DAG_CPC:  研究では未使用
- evaluate/
  - JSONexporter:       スケジュール結果をJSONに書き出します（研究では未使用）
  - make_compare_graph: 手法の有利不利比較グラフを生成します
  - make_graph        : x（変化させたパラメータ）と手法（legend）によって箱ひげ図を生成します
  - speed_up          : 関数名speedup_table、speedupを表示します
- Al_CCs         : 提案手法です。プロセッサコア割り当てをして、各ノードに開始時間を割り当てます
- DAG_Constructer: tgffファイル、またはNodeの配列からDAGを生成します
- DAG            : 実験で用いたDAGです。DAG_baseに加え、rta_cpf優先度決定手法が実装されています
- test           : tgffファイルと各種パラメータを受け取り、makespanを返します
