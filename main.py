# main.py
from CardGame import CardGame
import Simulation
from Statistic_Calculate import process_statistics_and_logs
def main():
    # デッキを定義
    deck = (
    # ストライク5枚
    [{"name": "Strike", "cost": 1} for _ in range(5)] +
    # 防御 4枚 
    [{"name": "Defend", "cost": 1} for _ in range(4)] +
    # 強打 1枚
    [{"name": "Bash", "cost": 2} for _ in range(1)] +
    # アセンダーの災厄
    [{"name": "Ascender's_Bane", "cost": 0}] +
    [{"name": "Carnage+", "cost": 2}]
    # # ヘモキネシス
    # [{"name": "Hemokinesis", "cost": 1} for _ in range(1)] +
    # # ダブルタップ+
    # [{"name": "Double_Tap+", "cost": 1}] +
    # # アイアンウェーブ
    # [{"name": "Iron_Wave", "cost": 1}] +
    # # ボディスラム+
    # [{"name": "Body_Slam+", "cost": 0}] +
    # # 大虐殺+
    # [{"name": "Carnage+", "cost": 2}] +
    # # ポンメルストライク+ 2枚
    # [{"name": "Pommel_Strike+", "cost": 1} for _ in range(2)] +
    # # 発火
    # [{"name": "Inflame", "cost": 1}] +
    # # 発火+
    # [{"name": "Inflame+", "cost": 1}]
    )
    deck2 = (
    # ストライク 5枚
    [{"name": "Strike", "cost": 1} for _ in range(5)] +
    # 防御 4枚 
    [{"name": "Defend", "cost": 1} for _ in range(4)] +
    # 強打 1枚
    [{"name": "Bash", "cost": 2} for _ in range(1)] +
    # アセンダーの災厄
    [{"name": "Ascender's_Bane", "cost": 0}]+
    [{"name": "Carnage+", "cost": 2}]+
     # サンダークラップ
    [{"name": "Thunderclap", "cost": 1}]
    )
    deck3 = (
    # ストライク 5枚
    [{"name": "Strike", "cost": 1} for _ in range(5)] +
    # 防御 4枚 
    [{"name": "Defend", "cost": 1} for _ in range(4)] +
    # 強打 1枚
    [{"name": "Bash", "cost": 2} for _ in range(1)] +
    [{"name": "Carnage+", "cost": 2}]+
    [{"name": "Strike+", "cost": 1} for _ in range(1)] +
    # アセンダーの災厄
    [{"name": "Ascender's_Bane", "cost": 0}]
    )
    game = CardGame(deck, MAX_ENERGY=4, END_TURN_NUM=4,name="初期に大虐殺+")
    game2 = CardGame(deck2, MAX_ENERGY=4, END_TURN_NUM=4,name="初期デッキに大虐殺+とサンダークラップ")
    game3 =  CardGame(deck3, MAX_ENERGY=4, END_TURN_NUM=4,name="初期デッキに大虐殺+とストライク+")
    #シミュレート
    games = [game, game2, game3]
    battle_logs, each_trial_damage_lists = Simulation.comparison(games,50,1)
    process_statistics_and_logs(games,battle_logs,each_trial_damage_lists)

if __name__ == "__main__":
    print("プログラム開始")
    main()
