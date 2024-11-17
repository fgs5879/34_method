# main.py
from Card import Card
from CardGame import CardGame
import card_details
import Simulation
import cProfile

def main():
    # デッキを定義
    deck = (
    # ストライク 2枚
    [Card("Strike", display_name="ストライク", cost=1, card_type='attack', damage=6) for _ in range(2)] +  
    # 防御 4枚
    [Card("Defend", display_name="防御", cost=1, card_type='skill',block=5) for _ in range(4)] +  
    # 強打
    [Card("Bash",display_name="強打", cost=2, card_type='attack', damage=8, vulnerable_turns=2)] 
    # アセンダーの災厄
    [Card("Ascender's_Bane",display_name="アセンダーの災厄", usable=False, card_type='curse', ethereal=True)] +
    #やせ我慢
    [Card("Power_Through", display_name="やせ我慢", card_type="skill", cost=1, block=15)] + 
    #ヘモキネシス
    [Card("Hemokinesis", display_name="ヘモキネシス", cost=1, card_type='attack', damage=15) for _ in range(1)] +
    #ダブルタップ+
    [Card("Double_Tap+", display_name="ダブルタップ+", card_type="skill",cost=1)] +
    #アイアンウェーブ
    [Card("Iron_Wave", display_name="アイアンウェーブ", cost=1, card_type='attack', damage=5, block=5) for _ in range(1)] +
    #ボディスラム+
    [Card("Body_Slam+", display_name="ボディスラム+", cost=0, card_type='attack') for _ in range(1)] +
    #大虐殺+
    [Card("Carnage+", display_name="大虐殺+", cost=2, card_type='attack', damage=28, ethereal=True) for _ in range(1)] +
    #焼身+
    [Card("Immolate+", display_name="焼身+", cost=2, card_type='attack', damage=28) for _ in range(1)] +
    #ポンメルストライク2枚
    [Card("Pommel_Strike+", display_name="ポンメルストライク+", cost=1, card_type='attack', damage=10, draw_num=2) for _ in range(2)] +
    #発火
    [Card("Inflame", display_name="発火", cost=1, card_type='power') for _ in range(1)] +
    発火+
    [Card("Inflame+", display_name="発火+", cost=1, card_type='power') for _ in range(1)] 
    )
    # ゲームの条件を定義(初期エナジー、戦闘ターン数)
    # デッキを定義
    # deck = (
    #     [{"name": "Strike", "cost": 1} for _ in range(5)] +  # ストライク 5枚
    #     [{"name": "Defend", "cost": 1} for _ in range(4)] +  # 防御 4枚
    #     [{"name": "Bash", "cost": 2}]  # 強打 1枚
    # )
    game = CardGame(deck, MAX_ENERGY=3, END_TURN_NUM=3)
    #シミュレート
    Simulation.concurrent_full_search(game, trials=1, lookahead_turns=2)

if __name__ == "__main__":
    print("プログラム開始")
    main()
