# Simulation.py
import statistics,time,tqdm,matplotlib.pyplot as plt
from Lookup import lookup
from utilies import get_playable_cards, duplicate_game
from CardGame import *
from card_details import *
import concurrent.futures
def concurrent_full_search(game:CardGame, trials:int, lookahead_turns:int):
    """並列処理を行う"""
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # タスクを submit で登録
        futures = [
            executor.submit(full_search_trial, game, trial, lookahead_turns)
            for trial in range(trials)
        ]
        
        battle_logs = []
        each_trial_damage_list = []
        
        # タスクが完了した順に結果を受け取る
        for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing trials"):
            result = future.result()
            battle_logs.append(result[0])
            each_trial_damage_list.append(result[1])
    # # results を展開
    # battle_logs = [result[0] for result in results]  # log_lines を収集
    # each_trial_damage_list = [result[1] for result in results]  # each_turn_damage_list を収集
    
    with open("logfile/battle_log.txt", "w",encoding="utf-8") as file:
        flat_battle_logs = [line for log in battle_logs for line in log]
        file.writelines(flat_battle_logs)

    turn_based_damage_list = [[] for _ in range(game.END_TURN_NUM)]

    for trial_damage in each_trial_damage_list:
        for turn_index, damage in enumerate(trial_damage):
            turn_based_damage_list[turn_index].append(damage)
    #統計記録txtfile出力用の文字列を保管
    statistics_lines = []
    #plt用のリスト
    turn_indices = []  # ターン番号
    mean_damage_list = []  # 各ターンの平均ダメージ
    population_variance_list = []  # 各ターンの母分散
    population_std_dev_list = []  # 各ターンの標準偏差
    plt.rcParams['font.family'] = 'MS Gothic'  # Windowsの場合の日本語フォント
    
    #基本的な情報
    statistics_lines.append("統計表示")
    statistics_lines.append(f"試行回数: {trials}\nターン数:{game.END_TURN_NUM}\n最大エナジー:{game.energy}\n")  # 最初に基本的な情報を出力
    battle_time = time.time()-start_time
    # 時間、分、秒に変換
    hours = int(battle_time // 3600)  # 時間の部分
    minutes = int((battle_time % 3600) // 60)  # 分の部分
    seconds = battle_time % 60  # 残りの秒数
    formatted_seconds = round(seconds, 2)  # 小数第2位まで表示
    statistics_lines.append(f"戦闘時間:{hours}時間{minutes}分{formatted_seconds}秒\n")
    statistics_lines.append("デッキ: " + ", ".join([get_card_detail(card["name"], "display_name") for card in game.draw_pile]) + "\n")

    
    # 統計結果をファイルに書き込み
    statistics_lines.append("各ターンのダメージ統計:\n\n")
    # 各ターンの統計データを計算して書き込む
    for turn_index, damage_list in enumerate(turn_based_damage_list, start=1):
        # 平均
        mean_damage = statistics.mean(damage_list)
         # 母分散
        population_variance = statistics.pvariance(damage_list)
        # 標準偏差（母集団のばらつきの指標として使用）
        population_std_dev = statistics.pstdev(damage_list)
        # ファイルに出力
        statistics_lines.append(f"ターン {turn_index}:\n")
        statistics_lines.append(f" 平均ダメージ: {mean_damage:.2f}\n")
        statistics_lines.append(f" 母分散: {population_variance:.2f}\n")
        statistics_lines.append(f" 標準偏差（ばらつきの指標）: {population_std_dev:.2f}\n")
        statistics_lines.append(f"平均ダメージ+-標準偏差:{mean_damage-population_std_dev:.2f} ~ {mean_damage+population_std_dev:.2f}\n")
        statistics_lines.append("============\n")
        #plt用のリストに格納
        turn_indices.append(turn_index)
        mean_damage_list.append(mean_damage)
        population_variance_list.append(population_variance)
        population_std_dev_list.append(population_std_dev)
    with open("logfile/statistics.txt", "w",encoding="utf-8") as file:
        file.writelines(statistics_lines)
    # グラフの作成
    plt.plot(turn_indices, mean_damage_list, label="平均ダメージ", marker='o', color='black')
    # 平均ダメージ + 標準偏差
    mean_plus_std_dev = [mean_damage + std_dev for mean_damage, std_dev in zip(mean_damage_list, population_std_dev_list)]
    plt.plot(turn_indices, mean_plus_std_dev, label="平均ダメージ + 標準偏差", linestyle='--', color='green')
    # 平均ダメージ - 標準偏差
    mean_minus_std_dev = [mean_damage - std_dev for mean_damage, std_dev in zip(mean_damage_list, population_std_dev_list)]
    plt.plot(turn_indices, mean_minus_std_dev, label="平均ダメージ - 標準偏差", linestyle='--', color='green')
    # グラフのタイトルとラベル
    plt.title('ターンごとのダメージと標準偏差')
    plt.xlabel('ターン')
    plt.ylabel('ダメージ')
    plt.legend()
    # 横軸の目盛りを1ずつに設定
    plt.xticks(range(min(turn_indices), max(turn_indices) + 1))
    # 平均ダメージ ± 標準偏差の数値をプロットに追加
    for i in range(len(turn_indices)):
        # 平均ダメージ ± 標準偏差
        plt.text(turn_indices[i], mean_plus_std_dev[i], f'{mean_plus_std_dev[i]:.2f}', ha='left', va='bottom', fontsize=20, color='red')
        plt.text(turn_indices[i], mean_minus_std_dev[i], f'{mean_minus_std_dev[i]:.2f}', ha='left', va='top', fontsize=20, color='red')
        # 平均ダメージの数字
        plt.text(turn_indices[i], mean_damage_list[i], f'{mean_damage_list[i]:.2f}', ha='center', va='bottom', fontsize=20, color='blue')
    # グリッド表示
    plt.grid(True)
    # グラフを表示
    plt.show()
            
def full_search_trial(game:CardGame, trial:int, lookahead_turns:int):
    random.shuffle(game.draw_pile)
    #統計用に各ターンごとに与えたダメージの合計を記録
    each_turn_damage_list = []
    #ログ記録用のリスト
    log_lines = []        
    log_lines.append(f"=== 1 ターン目開始===\n")
    
    start_turn(game)
    
    #指定ターン超過までwhileループし戦闘継続
    while game.turn_num <= game.END_TURN_NUM:
        #手札表示
        log_lines.append("手札: " + ", ".join([get_card_detail(card["name"],"display_name") for card in game.hand]) + "\n")
        #使用可能カードのリスト取得(end_turnを含む)
        playable_cards = get_playable_cards(game.hand, game.energy)
        #それぞれの選択ごとにゲームの先読みし、先読み先で与えたダメージをlistに格納。最も効果が高い選択を推測する
        #len(playable_cards) <= 1だと、playable_cards = はエンドターンだけであり、ターンエンドするしかない
        lookuped_damage_list = []
        #それぞれの選択ごとにゲームの先読みをする。
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(lookup, duplicate_game(game), played_card, lookahead_turns+game.turn_num)
                for played_card in playable_cards
                ]
            lookuped_damage_list = [future.result() for future in futures]
        #lookuped_damageの出力
        # for l, j in lookuped_damage_list:
        #     if(j  == "end_turn"):
        #         log_lines.append(str(l)+":"+str(j))
        #     else:
        #         log_lines.append(str(l)+":"+str(j.display_name))
        # log_lines.append("\n")
        max_damage, best_choice = max(lookuped_damage_list, key=lambda x: x[0])
        # 'best_choice'を実行する
        if best_choice["name"] == "end_turn":
            each_turn_damage_list.append(game.total_damage)
            end_turn(game)
            if game.turn_num > game.END_TURN_NUM:
                log_lines.append(f"\n=== 試行 {trial+1} 回目終了===\n与えた合計ダメージ:{game.total_damage}\n--------------------------------------\n")
            else:
                start_turn(game)
                log_lines.append(f"\n=== これまでのダメージ:{game.total_damage}===")
                if(game.e_vulnerable>0):
                    log_lines.append(f"\n=== 弱体:{game.e_vulnerable}===")
                if(game.p_strength>0):
                    log_lines.append(f"\n=== 筋力:{game.p_strength}===\n")
                log_lines.append(f"\n==={game.turn_num}ターン目開始===\n")  # ターン終了を記録
        else:
            log_lines.append(f"使用: {get_card_detail(best_choice['name'], 'display_name')}\n")  # 使用したカードの名前を記録
            use_card(game,best_choice)
    return (log_lines, each_turn_damage_list)
