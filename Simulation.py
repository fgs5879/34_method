# Simulation.py
import copy, statistics,time,matplotlib.pyplot as plt
from matplotlib import rcParams
from Lookup import lookup
from utilies import get_playable_cards
from CardGame import CardGame

class Simulation:
    def __init__(self, game, num_turns, trials, lookahead_turns):
        self.game = game
        self.num_turns = num_turns
        self.trials = trials
        self.lookahead_turns = lookahead_turns
    
    def full_search_trial(self):
        start_time = time.time()
        #統計用に各ターンごとに与えたダメージの合計を記録
        each_turn_damage_list = [[] for _ in range(self.num_turns)]
        # 結果を書き込むためのファイルを開く
        with open("battle_log.txt", "w",encoding="utf-8") as file:
            file.write(f"試行回数: {self.trials}\nターン数:{self.num_turns}\n")  # 最初に基本的な情報を出力
            file.write("デッキ: " + ", ".join([card.display_name for card in self.game.deck]) + "\n")
            for trial in range(self.trials):
                file.write(f"\n=== 試行 {trial+1} 回目開始===\n")
                #それぞれのtrialごとにゲームを作る
                this_game = CardGame(self.game.deck, self.game.MAX_ENERGY)
                file.write(f"\n=== 1 ターン目開始===\n")
                this_game.start_turn()
                
                #指定ターン超過までwhileループし戦闘継続
                while this_game.turn_num <= self.num_turns:
                    #手札表示
                    file.write("手札: " + ", ".join([card.display_name for card in this_game.hand]) + "\n")
                    #使用可能カードのリスト取得(end_turnを含む)
                    playable_cards = get_playable_cards(this_game.hand, this_game.energy)
                    #それぞれの選択ごとにゲームの先読みし、先読み先で与えたダメージをlistに格納。最も効果が高い選択を推測する
                    #len(playable_cards) <= 1だと、playable_cards = ["end_turn"]であり、ターンエンドするしかない
                    lookuped_damage_list = []
                    #それぞれの選択ごとにゲームの先読みをする。
                    for played_card in playable_cards:
                        simulate_game = copy.deepcopy(this_game)
                        lookuped_damage_list.append((lookup(simulate_game, played_card, self.lookahead_turns),played_card))
                    
                    max_damage, best_choice = max(lookuped_damage_list, key=lambda x: x[0])
                    # 'best_choice'を実行する
                    if best_choice == "end_turn":
                        each_turn_damage_list[this_game.turn_num-1].append(this_game.total_damage)
                        this_game.end_turn()
                        if this_game.turn_num > self.num_turns:
                            file.write(f"\n=== 試行 {trial+1} 回目終了===\n与えた合計ダメージ:{this_game.total_damage}\n")
                        else:
                            this_game.start_turn()
                            
                            file.write(f"\n=== これまでのダメージ:{this_game.total_damage}===")
                            file.write(f"\n=== 弱体:{this_game.sandbag.vulnerable}===")
                            file.write(f"\n=== 筋力:{this_game.player_strength}===\n")
                            file.write(f"\n==={this_game.turn_num}ターン目開始===\n")  # ターン終了を記録
                    else:
                        file.write(f"使用:{best_choice.display_name}\n")  # 使用したカードの名前を記録
                        this_game.use_card(best_choice)
        #plt用のリスト
        turn_indices = []  # ターン番号
        mean_damage_list = []  # 各ターンの平均ダメージ
        population_variance_list = []  # 各ターンの母分散
        population_std_dev_list = []  # 各ターンの標準偏差

        rcParams['font.family'] = 'MS Gothic'  # Windowsの場合の日本語フォント
        with open("statistics.txt", "w",encoding="utf-8") as file:
            #基本的な情報
            file.write("統計表示")
            file.write(f"試行回数: {self.trials}\nターン数:{self.num_turns}\n最大エナジー:{self.game.energy}\n")  # 最初に基本的な情報を出力
            battle_time = time.time()-start_time
            # 時間、分、秒に変換
            hours = int(battle_time // 3600)  # 時間の部分
            minutes = int((battle_time % 3600) // 60)  # 分の部分
            seconds = battle_time % 60  # 残りの秒数
            formatted_seconds = round(seconds, 2)  # 小数第2位まで表示
            file.write(f"戦闘時間:{hours}時間{minutes}分{formatted_seconds}秒\n")
            file.write("デッキ: " + ", ".join([card.display_name for card in self.game.deck]) + "\n")
            
            # 統計結果をファイルに書き込み
            file.write("各ターンのダメージ統計:\n\n")

            # 各ターンの統計データを計算して書き込む
            for turn_index, damage_list in enumerate(each_turn_damage_list, start=1):
                # 平均
                mean_damage = statistics.mean(damage_list)

                 # 母分散
                population_variance = statistics.pvariance(damage_list)

                # 標準偏差（母集団のばらつきの指標として使用）
                population_std_dev = statistics.pstdev(damage_list)

                # ファイルに出力
                file.write(f"ターン {turn_index}:\n")
                file.write(f" 平均ダメージ: {mean_damage:.2f}\n")
                file.write(f" 母分散: {population_variance:.2f}\n")
                file.write(f" 標準偏差（ばらつきの指標）: {population_std_dev:.2f}\n")
                file.write(f"平均ダメージ+-標準偏差:{mean_damage-population_std_dev:.2f} ~ {mean_damage+population_std_dev:.2f}\n")
                file.write("============\n")

                #plt用のリストに格納
                turn_indices.append(turn_index)
                mean_damage_list.append(mean_damage)
                population_variance_list.append(population_variance)
                population_std_dev_list.append(population_std_dev)

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
                



# ここにデバッグ用のコードを書きます。
if __name__ == "__main__":
    # 必要なクラスやデータをインポート（例：Card, Game, Sandbagなど）
    from Card import Card
    from CardGame import CardGame
    from Sandbag import Sandbag

    # ゲーム状態のシミュレート（手札、エナジー、カード等）
    deck = [
        Card("strike", cost=1, card_type='attack', damage=6),  # attackカード
        Card("strike", cost=1, card_type='attack', damage=6),  # attackカード
        Card("defend", cost=1, card_type='skill'),  # skillカード
        Card("bash", cost=2, card_type='attack', damage=8),  # attackカード
        Card("Inflame", cost=1, card_type='power')  # powerカード
    ]
    
    # 初期ゲーム状態を作成
    game = CardGame(deck)
    simulation = Simulation(game, num_turns=3, trials=3, lookahead_turns=1)
    
    # デバッグ用にmonメソッドを呼び出す
    simulation.full_search_trial()
