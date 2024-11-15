# Simulation.py
import copy,statistics,time,matplotlib.pyplot as plt
from Lookup import lookup
from utilies import get_playable_cards, duplicate_game
from CardGame import CardGame
from tqdm import tqdm
import concurrent.futures
def concurrent_full_search(game:CardGame, num_turns:int, trials:int, lookahead_turns:int):
    """並列処理を行う"""
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # `executor.map` で full_search_trial を実行
            results = list(
                tqdm(
                    executor.map(
                        full_search_trial,
                        [game] * trials,            # game を試行回数分コピー
                        [num_turns] * trials,       # num_turns を試行回数分コピー
                        range(trials),              # 各試行の trial_num
                        [lookahead_turns] * trials  # lookahead_turns を試行回数分コピー
                    ),
                    total=trials, desc="Progress"
                )
            )
    
    # results を展開
    battle_logs = [result[0] for result in results]  # log_lines を収集
    each_trial_damage_list = [result[1] for result in results]  # each_turn_damage_list を収集
    
    with open("battle_log.txt", "w",encoding="utf-8") as file:
        flat_battle_logs = [line for log in battle_logs for line in log]
        file.writelines(flat_battle_logs)

    turn_based_damage_list = [[] for _ in range(num_turns)]

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
    statistics_lines.append(f"試行回数: {trials}\nターン数:{num_turns}\n最大エナジー:{game.energy}\n")  # 最初に基本的な情報を出力
    battle_time = time.time()-start_time
    # 時間、分、秒に変換
    hours = int(battle_time // 3600)  # 時間の部分
    minutes = int((battle_time % 3600) // 60)  # 分の部分
    seconds = battle_time % 60  # 残りの秒数
    formatted_seconds = round(seconds, 2)  # 小数第2位まで表示
    statistics_lines.append(f"戦闘時間:{hours}時間{minutes}分{formatted_seconds}秒\n")
    statistics_lines.append("デッキ: " + ", ".join([card.display_name for card in game.deck]) + "\n")
    
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
    with open("statistics.txt", "w",encoding="utf-8") as file:
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
        plt.text(turn_indices[i], mean_plus_std_dev[i], f'{mean_plus_std_dev[i]:.2f}', ha='left', va='bottom', fontsize=12, color='red')
        plt.text(turn_indices[i], mean_minus_std_dev[i], f'{mean_minus_std_dev[i]:.2f}', ha='left', va='top', fontsize=12, color='red')
        # 平均ダメージの数字
        plt.text(turn_indices[i], mean_damage_list[i], f'{mean_damage_list[i]:.2f}', ha='center', va='bottom', fontsize=12, color='blue')
    # グリッド表示
    plt.grid(True)
    
    # グラフを表示
    plt.show()
            


def full_search_trial(game:CardGame, num_turns:int, trial:int, lookahead_turns:int):
    #統計用に各ターンごとに与えたダメージの合計を記録
    each_turn_damage_list = []
    #ログ記録用のリスト
    log_lines = []        
    #それぞれのtrialごとにゲームを作る
    this_game = CardGame(game.deck, game.MAX_ENERGY)
    log_lines.append(f"\n=== 1 ターン目開始===\n")
    this_game.start_turn()
    
    #指定ターン超過までwhileループし戦闘継続
    while this_game.turn_num <= num_turns:
        #手札表示
        log_lines.append("手札: " + ", ".join([card.display_name for card in this_game.hand]) + "\n")
        #使用可能カードのリスト取得(end_turnを含む)
        playable_cards = get_playable_cards(this_game.hand, this_game.energy)
        #それぞれの選択ごとにゲームの先読みし、先読み先で与えたダメージをlistに格納。最も効果が高い選択を推測する
        #len(playable_cards) <= 1だと、playable_cards = ["end_turn"]であり、ターンエンドするしかない
        lookuped_damage_list = []
        #それぞれの選択ごとにゲームの先読みをする。
        for played_card in playable_cards:
            lookuped_damage_list.append((lookup(duplicate_game(this_game), played_card, lookahead_turns),played_card))
        
        max_damage, best_choice = max(lookuped_damage_list, key=lambda x: x[0])
        # 'best_choice'を実行する
        if best_choice == "end_turn":
            each_turn_damage_list.append(this_game.total_damage)
            this_game.end_turn()
            if this_game.turn_num > num_turns:
                log_lines.append(f"\n=== 試行 {trial+1} 回目終了===\n与えた合計ダメージ:{this_game.total_damage}\n")
            else:
                this_game.start_turn()
                log_lines.append(f"\n=== これまでのダメージ:{this_game.total_damage}===")
                if(this_game.sandbag.vulnerable>0):
                    log_lines.append(f"\n=== 弱体:{this_game.sandbag.vulnerable}===")
                if(this_game.player_strength>0):
                    log_lines.append(f"\n=== 筋力:{this_game.player_strength}===\n")
                log_lines.append(f"\n==={this_game.turn_num}ターン目開始===\n")  # ターン終了を記録
        else:
            log_lines.append(f"使用:{best_choice.display_name}\n")  # 使用したカードの名前を記録
            this_game.use_card(best_choice)
    return (log_lines, each_turn_damage_list)