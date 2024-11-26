import statistics
import matplotlib.pyplot as plt
from CardGame import CardGame
from card_details import get_card_detail
import matplotlib.pyplot as plt
import statistics

def process_statistics_and_logs(games: list[CardGame], battle_logs: list[str], each_trial_damage_lists: list[float]):
    """複数のゲームインスタンスに対して統計処理とログ書き出しを行い、結果を比較する"""
    plt.rcParams['font.family'] = 'MS Gothic'  
    trials = len(each_trial_damage_lists[0])
    statistics_lines_list = []
    # グラフのカスタマイズ
    plt.figure(figsize=(14, 10))  # グラフサイズ設定
    plt.title('ターンごとのダメージと標準偏差')
    plt.xlabel('ターン')
    plt.ylabel('ダメージ')
    plt.xticks(range(1, games[0].END_TURN_NUM + 1))
    plt.grid(True)

    color_list = ["red", "blue","green","black"]
    # 各ゲームインスタンスについて処理
    for index, (game, battle_log, each_trial_damage_list) in enumerate(zip(games, battle_logs, each_trial_damage_lists)):
        # ログファイル出力
        with open("logfile/battle_log_"+game.name+".txt", "w", encoding="utf-8") as file:
            flat_battle_logs = [line for log in battle_log for line in log]
            file.writelines(flat_battle_logs)

        # 各ターンごとのダメージリストに変換
        turn_based_damage_list = [[] for _ in range(game.END_TURN_NUM)]
        for trial_damage in each_trial_damage_list:
            for turn_index, damage in enumerate(trial_damage):
                turn_based_damage_list[turn_index].append(damage)

        # 統計情報の準備
        statistics_lines = []
        turn_indices = []
        mean_damage_list = []
        population_variance_list = []
        population_std_dev_list = []

        # 基本的な情報
        statistics_lines.append(f"ゲーム: {game.name}\n")  # ゲーム名（もしあれば）
        statistics_lines.append(f"試行回数: {trials}\nターン数: {game.END_TURN_NUM}\n最大エナジー: {game.energy}\n")
        statistics_lines.append("デッキ: " + ", ".join([get_card_detail(card["name"], "display_name") for card in game.draw_pile]) + "\n")

        # 各ターンの統計情報を収集
        for turn_index, damage_list in enumerate(turn_based_damage_list, start=1):
            mean_damage = statistics.mean(damage_list)
            population_variance = statistics.pvariance(damage_list)
            population_std_dev = statistics.pstdev(damage_list)

            # 統計データを格納
            statistics_lines.append(f"ターン {turn_index}:\n")
            statistics_lines.append(f" 平均ダメージ: {mean_damage:.2f}\n")
            statistics_lines.append(f" 標準偏差: {population_std_dev:.2f}\n")
            statistics_lines.append(f" 平均ダメージ±標準偏差: {mean_damage - population_std_dev:.2f} ~ {mean_damage + population_std_dev:.2f}\n")
            statistics_lines.append("============\n")

            # グラフ用データ
            turn_indices.append(turn_index)
            mean_damage_list.append(mean_damage)
            population_variance_list.append(population_variance)
            population_std_dev_list.append(population_std_dev)
            
        # 統計情報を集める
        statistics_lines_list.append(statistics_lines)
        
        
        # 各ゲームの結果をグラフに追加
        plt.plot(turn_indices, mean_damage_list, label=f"平均ダメージ ({game.name})", marker='o', color=color_list[index])
        mean_plus_std_dev = [mean_damage + std_dev for mean_damage, std_dev in zip(mean_damage_list, population_std_dev_list)]
        plt.plot(turn_indices, mean_plus_std_dev, label=f"平均 + 標準偏差 ({game.name})", linestyle='--',color=color_list[index])
        mean_minus_std_dev = [mean_damage - std_dev for mean_damage, std_dev in zip(mean_damage_list, population_std_dev_list)]
        plt.plot(turn_indices, mean_minus_std_dev, label=f"平均 - 標準偏差 ({game.name})", linestyle='--',color=color_list[index])

    # 統計情報の書き出し
    with open("logfile/statistics.txt", "w", encoding="utf-8") as file:
        for statistics_lines in statistics_lines_list:
            file.writelines(statistics_lines)

    # グラフを表示
    plt.legend()
    plt.show()
