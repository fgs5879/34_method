import CardGame
from utilies import get_playable_cards, duplicate_game
def lookup(game:CardGame, used_card, lookahead_turns):
    """
    ゲームの状態と選択されたカードを受け取り、
    選択されたカードが使用された場合のゲームをlookup_turnだけ先読みし、先読みの中で与えたダメージを返す。
    used_cardには"end_turn"という文字列が入ることがあり、その場合は使用できるカードがあるがターンエンドする。
    再帰関数である。
    """
    first_turn_num = game.turn_num #先読み開始時のターン数
    #選択をこのlookup内で実行
    #end_turnが選ばれた場合ターン終了する。lookahead_turnsを超えた場合、この推測での合計ダメージを返す。
    if used_card == "end_turn":
        game.end_turn()
        lookahead_turns -=1
        if game.turn_num > first_turn_num + lookahead_turns:
            return game.total_damage
        game.start_turn()
    #そのカードを使用してみる
    else:
        game.use_card(used_card)

    #使用可能カードリストを得る
    playable_cards = get_playable_cards(game.hand, game.energy)

    #それぞれの選択ごとにゲームの先読みし、先読み先で与えたダメージをlistに格納。最も効果が高い選択を推測する
    #len(playable_cards) <= 1だと、playable_cards = ["end_turn"]であり、ターンエンドするしかない
    lookuped_damage_list = []
    for played_card in playable_cards:
        simulated_game = duplicate_game(game)
        lookuped_damage_list.append((lookup(simulated_game, played_card, lookahead_turns), played_card))
    
    max_damage, best_choice = max(lookuped_damage_list, key=lambda x: x[0])
    return lookup(game, best_choice, lookahead_turns)

        

        

        
if __name__ == "__main__":
    # ゲームのインスタンスを作成（必要に応じてセットアップ）
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
    game.start_turn()
    # 使用するカードの例
    used_card = game.hand[0]  # 例えば、手札の最初のカードを使用

    # 先読みターン数
    lookahead_turns = 2
    print(used_card)
    # lookup関数の呼び出し
    print(lookup(game, used_card, lookahead_turns), used_card)


