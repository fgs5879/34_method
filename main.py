# main.py
from Card import Card
from CardGame import CardGame
from Simulation import Simulation
import cProfile

def main():
    # ゲーム状態のシミュレート（手札、エナジー、カード等）
    deck = (
    [Card("Strike", display_name="ストライク", cost=1, card_type='attack', damage=6) for _ in range(5)] +  # Strikeカード 5枚
    [Card("Defend", display_name="防御", cost=1, card_type='skill') for _ in range(4)] +  # Defendカード 4枚
    [Card("Bash",display_name="強打", cost=2, card_type='attack', damage=8, vulnerable_turns=2)] +  # Bashカード 1枚
    [Card("Ascender's_Bane",display_name="アセンダーの災厄", usable=False, card_type='curse')]  # Ascender's Bane 1枚
    )
    # 初期ゲーム状態を作成
    game = CardGame(deck, MAX_ENERGY=3)
    simulation = Simulation(game, num_turns=3, trials=50, lookahead_turns=2)
    
    #シミュレート
    simulation.full_search_trial()

if __name__ == "__main__":
    main()