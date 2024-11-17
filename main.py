# main.py
from CardGame import CardGame
import Simulation

def main():
    # デッキを定義
    deck = (
    # ストライク 2枚
    [{"name": "Strike", "cost": 1} for _ in range(2)] +
    # 防御 4枚 
    [{"name": "Defend", "cost": 1} for _ in range(4)] +
    # 強打 1枚
    [{"name": "Bash", "cost": 2} for _ in range(1)] +
    # アセンダーの災厄
    [{"name": "Ascender's_Bane", "cost": 0}] +
    # ヘモキネシス
    [{"name": "Hemokinesis", "cost": 1} for _ in range(1)] +
    # ダブルタップ+
    [{"name": "Double_Tap+", "cost": 1}] +
    # アイアンウェーブ
    [{"name": "Iron_Wave", "cost": 1}] +
    # ボディスラム+
    [{"name": "Body_Slam+", "cost": 0}] +
    # 大虐殺+
    [{"name": "Carnage+", "cost": 2}] +
    # ポンメルストライク+ 2枚
    [{"name": "Pommel_Strike+", "cost": 1} for _ in range(2)] +
    # 発火
    [{"name": "Inflame", "cost": 1}] +
    # 発火+
    [{"name": "Inflame+", "cost": 1}]
    )
    game = CardGame(deck, MAX_ENERGY=4, END_TURN_NUM=4)
    #シミュレート
    Simulation.concurrent_full_search(game, trials=50, lookahead_turns=1)

if __name__ == "__main__":
    print("プログラム開始")
    main()
