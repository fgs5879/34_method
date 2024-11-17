# 34_method
概要は動画をご覧ください。
先駆者が存在すると思いますので、ご利用は自由です。(そもそも数日で作れるので、そこまで価値もないと思いますが)

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

Lookup.py
  lookahead_end_turnsで指定したターンに到達するか、戦闘終了までの、取り得るプレイを全探索します。再帰を使用します。

utilies.py
  他のファイルから呼び出される関数をいくつか記述しています。
  get_playtable_cards関数は手札とエナジーから使用可能カードを返します。
  remove_duplicate_cards関数は重複したカードを削除したリストを返します。(コンピュータの思考ルーチンにとって、同じカードはまとめても問題ありません。しかし、カードの名前とコストが一致したら同じと定義していますが、機能を増やす場合は不十分です)
  duplicate_game関数はゲームを複製します。単純にcopy.copyやcopy.deepcopyではそれぞれ弊害があります。  

battlelog.txtは戦闘ログです
statistics.txtは戦闘の統計です。
