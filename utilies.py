import copy
#他の自作pyファイルからimportされる関数を記述する
def get_playable_cards(hand, energy):
        
        """
        与えられた手札とエナジーに基づいて、使用可能なカードのリストを返す関数。
        """
        #コストと名前の一致するカードをまとめる。
        unique_hand = remove_duplicate_cards(hand)

        playable_cards = ["end_turn"]
        #使用可能カードリストを得る
        for card in unique_hand:
            if card.usable == True and card.cost <= energy:
                playable_cards.append(card)

        return playable_cards

def remove_duplicate_cards(card_list):
    # name と cost を基準に重複を排除
    seen = set()
    unique_cards = []
    
    for card in card_list:
        card_key = (card.name, card.cost)  # name と cost を組み合わせてキーに
        if card_key not in seen:
            seen.add(card_key)
            unique_cards.append(card)
    
    return unique_cards

def duplicate_game(game):
    """gameを複製する"""
    # duplicated_game = copy.deepcopy(game)
    # リストやオブジェクトを手動で初期化（シャローコピーではなく、ディープコピー）
    duplicated_game = copy.copy(game)
    duplicated_game.hand = game.hand[:]
    duplicated_game.discard_pile = game.discard_pile[:]
    duplicated_game.exhaust_pile = game.exhaust_pile[:]
    duplicated_game.deck = game.deck[:]
    return duplicated_game
