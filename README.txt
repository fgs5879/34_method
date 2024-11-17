# 34_method
概要は動画をご覧ください。

各ファイルの説明をします。
main.py
  基本的にこのファイルを実行して動作させます。
  デッキを定義し、CardGameインスタンスを作成し、シミュレーションします。

card_details.py
  カードの情報を定義します。
  新カードを追加したい場合このファイルに追記してください。
  CARD_DETAILS内で定義されていない属性はDEFAULT_CARD_DETAILSの値が割り当てられます。

CardGame.py
  class CardGameはその戦闘の情報を管理します。
  同ファイルの他の関数は全てCardGameのインスタンスを引数に取り、何らかの処理を行います。

Simulation.py
  実際に戦闘のシミュレーションを行います。
  main.pyからconcurrent_full_search関数が呼び出されます。
  concurrent_full_search関数は指定回数だけfull_search_trial関数を並列処理で実行し、結果に対し統計関係の計算やグラフの出力をします。
  full_search_trial関数は戦闘シミュレーションをします。lookup関数を呼び出しプレイを決定します。
    battlelog.txtファイルへの出力も実行します。
    
