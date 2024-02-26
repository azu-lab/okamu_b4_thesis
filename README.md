# 卒業研究(okamu)

## ディレクトリ構成
- DAG/
  - TGFFのファイル（.tgff）が格納されています
  - Edgeは出エッジ数pを3~6に変化させたもの
  - Nodeはノード数を20~100に変化させたもの
- DATA/
  - 計算したmakespanなどのデータを保存したyamlが格納されます
  - ディレクトリは変更させたパラメータです
- Image/
  - 生成した画像が格納されます
  - ディレクトリは変更させたパラメータです
- python/
  - 実装に用いたプログラムファイルを格納しています
  - 詳しい内容は、python/readme.mdを参照してください
- test_rta_cpf_priority.ipynb
  - 優先度決定手法rta_cpf（既存手法）のテストです
- test_varying_xxx.ipynb
  - xxxを変更して評価を行います
  - Run Allで、必要なグラフが生成されます
  - test_varying_node.ipynbには、論文では使っていない手法の有利比較とspeedup計算が入っています

## 提案手法について
python/README.md に簡単なまとめを書いています
